import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date, timedelta
from datetime import datetime
from core import database
from core import discord_utils as utils
from core.server_config import server_config


class Moderator(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.log_channel = server_config["log_channel"]

    # Check if they are allowed to kick people, if so kick them
    # Kick

    @commands.command(description="Kicks a user from the server.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason="No reason given."):
        """
        kick (mention user here) (reason)
        """

        if user.guild_permissions.administrator:
            await utils.error_embed(ctx, "Command Permission Error!", {"Details": "`You cannot kick this member. They are an administrator.`"})
            self.client.dispatch("command_failed", ctx)
            return

        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator=ctx.author.id, date=date.today(), reason=reason, action = "KICK")

        await user.kick(reason=reason)
        await utils.successful_embed(self.client.get_channel(self.log_channel), "Kick Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx)
    # Check if they are allowed to ban people, if so ban them
    # Ban && UnBan

    @commands.command(description="Bans a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason given."):
        """
        ban (mention user here) (reason)
        """

        if user.guild_permissions.administrator:
            await utils.error_embed(ctx, "Command Permission Error!",
                                    {"Details": "`You cannot ban this member. They are an administrator.`"})
            self.client.dispatch("command_failed", ctx)
            return

        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        if database_query:
            await utils.error_embed(ctx, "Command Error!",
                                    {"Details": f"`{user} is already banned.`"})
            self.client.dispatch("command_failed", ctx)
            return

        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator=ctx.author.id, date=date.today(), reason=reason, action = "BAN")

        await user.ban(reason=reason)
        await utils.successful_embed(self.client.get_channel(self.log_channel), "Ban Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx)

    @ commands.command(description="Unbans a user.")
    @ commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: str, *, reason="No reason given."):
        """
        unban (username and #number) (reason)
        """

        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        if not database_query:
            await utils.error_embed(ctx, "Search Error!",
                                    {"Details": f'`Cannot find {user}.`'})
            self.client.dispatch("command_failed", ctx)

        id = database_query.get().user_id
        banned_users = await ctx.guild.bans()

        database_query.get().delete_instance()

        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator=ctx.author.id, date=date.today(), reason=reason, action = "UNBAN")

        for ban_entry in banned_users:
            if ban_entry.user.id == id:
                await ctx.guild.unban(ban_entry.user)
                await utils.successful_embed(self.client.get_channel(self.log_channel), "Unban Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
                self.client.dispatch("command_successful", ctx)
                break

    # Warn && UnWarn
    # If has been warned 3 times, kick them.
    @ commands.command(description="Warns a user and kicks them if they have more than three warnings.")
    @ commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: discord.Member, *, reason="No reason given."):
        """
        warn (mention user here) (reason)
        """
        if user.guild_permissions.administrator:
            await utils.error_embed(ctx, "Command Permission Error!",
                                    {"Details": "`You cannot warn this member. They are an administrator.`"})
            self.client.dispatch("command_failed", ctx)
            return

        # Add to database
        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator=ctx.author.id, date=date.today(), reason=reason, action = "WARN")

        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        await utils.successful_embed(self.client.get_channel(self.log_channel), "Warn Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx)

        if len(database_query) >= 3:
            database_query.get().delete_instance()
            await self.kick(ctx, user, reason="User has been warned three times.")

    @ commands.command(description="Unwarns the user and erases all the user's previous warnings.")
    @ commands.has_permissions(kick_members=True)
    async def unwarn(self, ctx, user: discord.Member, *, reason="No reason given."):
        """
        unwarn (mention user here) (reason)
        """
        # Add to database
        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        if not database_query:
            await utils.error_embed(ctx, "Search Error!",
                                    {"Details": f'`{user} has not been warned before.`'})
            self.client.dispatch("command_failed", ctx)
            return

        database_query.get().delete_instance()
        await utils.successful_embed(self.client.get_channel(self.log_channel), "Unwarn Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx)

    @ commands.command(description="Removes a given users messages.")
    @ commands.has_permissions(kick_members=True, ban_members=True)
    async def purge(self, ctx, user: discord.Member, amount: int):
        """
        purge (mention user here) (amount of text to remove)
        """

        await ctx.channel.purge(limit=amount, check=lambda message: message.author == user)
        await utils.successful_embed(self.client.get_channel(self.log_channel), "Purge Results", user=user, moderator=ctx.author, details={"Details": f'Amount: `{amount}`'})
        self.client.dispatch("command_successful", ctx)

    @ commands.command(description="Mutes a user for a specified amount of time.")
    @ commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, time: int, *, reason="No reason given."):
        """
        mute (mention user here) (how many minutes to mute) (reason)
        """
        if user.guild_permissions.administrator:
            await utils.error_embed(ctx, "Command Permission Error!", {"Details": "`You cannot mute this member. They are an administrator.`"})
            self.client.dispatch("command_failed", ctx)
            return
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role in user.roles:
            await utils.error_embed(ctx, "Muting Error!", {"Details": "`This user is already muted.`"})
            self.client.dispatch("command_failed", ctx)
            return

        timestamp = datetime.now()
        unmute_timestamp = timestamp + timedelta(minutes=time)

        current_time = timestamp.strftime(r'%m/%d, %H:%M')
        unmute_time = unmute_timestamp.strftime(r'%m/%d, %H:%M')

        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator=ctx.author.id, date=date.today(), reason=reason, action = "MUTE")

        await user.add_roles(muted_role)
        await utils.successful_embed(self.client.get_channel(self.log_channel), "Mute Results", user, ctx.author, {"Details": f'Duration: `{time}m`'}, reason)
        self.client.dispatch("command_successful", ctx)

    @ commands.command(description="Unmutes a user.")
    @ commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        """
        unmute (mention user here)
        """
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        muted_user = database.MutedUser.select().where(
            (database.MutedUser.username == user))

        if not muted_user:
            await utils.error_embed(ctx, "Unmuting Error!", {"Details": "`User is not muted!`"})
            self.client.dispatch("command_failed", ctx)
            return

        muted_user.get().delete_instance()
        await utils.successful_embed(self.client.get_channel(self.log_channel), "Unmute Results", user=user, moderator=ctx.author, details={"Details": f'`{user} has been umuted`'})
        await user.remove_roles(muted_role)
        self.client.dispatch("command_successful", ctx)

    @commands.command(description="Check the latency of the bot.")
    async def ping(self, ctx):
        """
        ping
        """
        await utils.send_embed(ctx, "Latency ⌛", [{"Current Ping": f'{round(self.client.latency * 1000)}ms'}])
        self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(Moderator(client))

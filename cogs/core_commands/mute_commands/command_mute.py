import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date, timedelta
from datetime import datetime
from core import database
from core import discord_utils as utils
from core.server_config import server_config


class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @ commands.command(description="Mutes a user for a specified amount of time.")
    @ commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, time: str = "45m", *, reason="No reason given."):
        """
        mute (mention user here) (how long to mute {s, m, h, d}) (reason)
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

        current_time = timestamp.strftime(r'%m/%d, %H:%M')
        unmute_time = utils.showFutureTime(time)

        database.MutedUser.create(
            username=user,
            user_id=user.id,
            moderator_id=ctx.author.id, date=date.today(), reason=reason, action="MUTE", time_muted=current_time, mute_time_release=unmute_time)
        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator_id=ctx.author.id, date=date.today(), reason=reason, action="MUTE")

        await user.add_roles(muted_role)
        await utils.successful_embed([ctx, self.client.get_channel(self.log_channel)], "Mute Results", user, ctx.author, {"Details": f'Duration: `{time}`'}, reason)
        self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(Mute(client))

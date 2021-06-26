from core.server_config import server_config
from core import discord_utils as utils
from core import database
from datetime import datetime
from datetime import date, timedelta
from discord.ext import tasks
from discord.ext import commands
import discord


class UnMute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Unmutes a user.")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member, *, reason="No reason given."):
        """
        unmute (mention user here) reason
        """
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        muted_user = database.MutedUser.select().where(
            (database.MutedUser.user_id == user.id))
        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator_id=ctx.author.id, date=date.today(), reason=reason, action="UNMUTE")

        if not muted_user:
            await utils.error_embed(ctx, "Unmuting Error!", {"Details": "`User is not muted!`"})
            self.client.dispatch("command_failed", ctx)
            return

        muted_user.get().delete_instance()
        await utils.successful_embed([ctx, self.client.get_channel(self.log_channel)], "Unmute Results", user=user, moderator=ctx.author, details={"Details": f'`{user} has been umuted`'})
        await user.remove_roles(muted_role)
        self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(UnMute(client))

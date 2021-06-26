import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date, timedelta
from datetime import datetime
from core import database
from core import discord_utils as utils
from core.server_config import server_config


class Kick(commands.Cog):
    def __init__(self, client):
        self.client = client

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
            moderator_id=ctx.author.id, date=date.today(), reason=reason, action="KICK")

        await user.kick(reason=reason)
        await utils.successful_embed([ctx, self.client.get_channel(self.log_channel)], "Kick Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(Kick(client))

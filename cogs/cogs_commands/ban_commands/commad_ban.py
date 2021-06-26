import discord
from discord.ext import commands
from datetime import date
from core import database
from core.utils import embed_utils as utils


class Ban(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Bans a user from the server.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason="No reason given."):
        """
        ban (mention user here) (reason)
        """

        if user.guild_permissions.administrator:
            error_embed = utils.error_embed(ctx, "Command Permission Error!",
                                            {"Details": "`You cannot ban this member. They are an administrator.`"})
            self.client.dispatch("command_failed", ctx, error_embed)
            return

        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        if database_query:
            error_embed = utils.error_embed(ctx, "Command Error!",
                                            {"Details": f"`{user} is already banned.`"})
            self.client.dispatch("command_failed", ctx, error_embed)
            return

        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator_id=ctx.author.id, date=date.today(), reason=reason, action="BAN")

        await user.ban(reason=reason)
        successful_embed = utils.successful_embed("Ban Results", user, ctx.author, {
                                                  "Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx, successful_embed)


def setup(client):
    client.add_cog(Ban(client))

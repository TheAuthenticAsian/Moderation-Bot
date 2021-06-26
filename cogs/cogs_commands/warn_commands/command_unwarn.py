import discord
from discord.ext import commands
from datetime import date
from core import database
from core.utils import embed_utils as utils


class UnWarn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Unwarns the user and erases all the user's previous warnings.")
    @commands.has_permissions(kick_members=True)
    async def unwarn(self, ctx, user: discord.Member, *, reason="No reason given."):
        """
        unwarn (mention user here) (reason)
        """
        # Add to database
        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        if not database_query:
            error_embed = utils.error_embed(ctx, "Search Error!",
                                            {"Details": f'`{user} has not been warned before.`'})
            self.client.dispatch("command_failed", ctx, error_embed)
            return

        for q in database_query:
            q.delete_instance()
        successful_embed = utils.successful_embed("Unwarn Results", user, ctx.author, {
                                                  "Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx, successful_embed)


def setup(client):
    client.add_cog(UnWarn(client))

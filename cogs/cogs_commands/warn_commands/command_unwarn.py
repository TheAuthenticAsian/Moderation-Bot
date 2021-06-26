import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date, timedelta
from datetime import datetime
from core import database
from core import discord_utils as utils
from core.server_config import server_config


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
            await utils.error_embed(ctx, "Search Error!",
                                    {"Details": f'`{user} has not been warned before.`'})
            self.client.dispatch("command_failed", ctx)
            return

        for q in database_query:
            q.delete_instance()
        await utils.successful_embed([ctx, self.client.get_channel(self.log_channel)], "Unwarn Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(UnWarn(client))

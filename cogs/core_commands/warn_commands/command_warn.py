import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date, timedelta
from datetime import datetime
from core import database
from core import discord_utils as utils
from core.server_config import server_config


class Warn(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Warns a user and kicks them if they have more than three warnings.")
    @commands.has_permissions(kick_members=True)
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
            moderator_id=ctx.author.id, date=date.today(), reason=reason, action="WARN")

        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        await utils.successful_embed([ctx, self.client.get_channel(self.log_channel)], "Warn Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
        self.client.dispatch("command_successful", ctx)

        if len(database_query) >= 3:
            for q in database_query:
                q.delete_instance()
            await self.kick(ctx, user, reason="User has been warned three times.")


def setup(client):
    client.add_cog(Warn(client))

from discord.ext import commands
from datetime import date
from core import database
from core.utils import embed_utils as utils


class UnBan(commands.Cog):
    def __init__(self, client):
        self.client = client

    @ commands.command(description="Unbans a user.")
    @ commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: str, *, reason="No reason given."):
        """
        unban (username and #number) (reason)
        """

        database_query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        if not database_query:
            error_embed = utils.error_embed(ctx, "Search Error!",
                                            {"Details": f'`Cannot find {user}.`'})
            self.client.dispatch("command_failed", ctx, error_embed)

        id = database_query.get().user_id
        banned_users = await ctx.guild.bans()

        database_query.get().delete_instance()

        database.ModerationLogs.create(
            username=user,
            user_id=user.id,
            moderator_id=ctx.author.id, date=date.today(), reason=reason, action="UNBAN")

        for ban_entry in banned_users:
            if ban_entry.user.id == id:
                await ctx.guild.unban(ban_entry.user)
                successful_embed = utils.successful_embed([ctx, self.client.get_channel(
                    self.log_channel)], "Unban Results", user, ctx.author, {"Details": f'Date: `{date.today()}`'}, reason)
                self.client.dispatch("command_successful",
                                     ctx, successful_embed)
                break


def setup(client):
    client.add_cog(UnBan(client))

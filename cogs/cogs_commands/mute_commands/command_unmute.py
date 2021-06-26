from core import database
from datetime import date
from discord.ext import commands
from core.utils import embed_utils
from core.utils import time_utils
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
            error_embed = embed_utils.error_embed(ctx, "Unmuting Error!", {
                "Details": "`User is not muted!`"})
            self.client.dispatch("command_failed", ctx, error_embed)
            return

        muted_user.get().delete_instance()
        await user.remove_roles(muted_role)
        successful_embed = embed_utils.successful_embed("Unmute Results", user=user, moderator=ctx.author, details={
            "Details": f'`{user} has been umuted`'})
        self.client.dispatch("command_successful", ctx, successful_embed)


def setup(client):
    client.add_cog(UnMute(client))

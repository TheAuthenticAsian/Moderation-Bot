import discord
from discord.ext import commands
from core.utils import embed_utils as utils


class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Removes a given users messages.")
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def purge(self, ctx, amount: int, user: discord.Member = None):
        """
        purge (amount of text to remove *limit is 40*) (mention user here *optional*) 

        """

        if amount > 40:
            amount = 40

        if user:
            await ctx.channel.purge(limit=amount, check=lambda message: message.author == user)
            successful_embed = utils.successful_embed(
                "Purge Results", user=user, moderator=ctx.author, details={"Details": f'Amount: `{amount}`'})
        else:
            await ctx.channel.purge(limit=amount)
            successful_embed = utils.successful_embed(
                "Purge Results", user=None, moderator=ctx.author, details={"Details": f'Amount: `{amount}`'})

        self.client.dispatch("command_successful", ctx, successful_embed)


def setup(client):
    client.add_cog(Purge(client))

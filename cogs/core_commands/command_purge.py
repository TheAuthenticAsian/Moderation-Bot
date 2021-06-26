import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date, timedelta
from datetime import datetime
from core import database
from core import discord_utils as utils
from core.server_config import server_config


class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Removes a given users messages.")
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def purge(self, ctx, amount: int = 10, user: discord.Member = None):
        """
        purge (amount of text to remove *default is 10*) (mention user here *optional*) 

        """

        if user:
            await ctx.channel.purge(limit=amount, check=lambda message: message.author == user)
            await utils.successful_embed([ctx, self.client.get_channel(self.log_channel)], "Purge Results", user=user, moderator=ctx.author, details={"Details": f'Amount: `{amount}`'})
        else:
            await ctx.channel.purge(limit=amount)
            await utils.successful_embed([ctx, self.client.get_channel(self.log_channel)], "Purge Results", user=None, moderator=ctx.author, details={"Details": f'Amount: `{amount}`'})


def setup(client):
    client.add_cog(Purge(client))

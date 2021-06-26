from discord.ext import commands
from core.utils import embed_utils as utils


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Check the latency of the bot.")
    async def ping(self, ctx):
        """
        ping
        """
        embed = utils.create_base_embed(
            "Latency ⌛", [{"Current Ping": f'{round(self.client.latency * 1000)}ms'}])
        await ctx.send(embed=embed)
        await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Ping(client))

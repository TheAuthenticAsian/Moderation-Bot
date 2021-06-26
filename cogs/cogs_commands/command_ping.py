import discord
from discord.ext import commands
from discord.ext import tasks
from datetime import date, timedelta
from datetime import datetime
from core import database
from core import discord_utils as utils
from core.server_config import server_config


class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description="Check the latency of the bot.")
    async def ping(self, ctx):
        """
        ping
        """
        await utils.send_embed(ctx, "Latency ⌛", [{"Current Ping": f'{round(self.client.latency * 1000)}ms'}])
        self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(Ping(client))

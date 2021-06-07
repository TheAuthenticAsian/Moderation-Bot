import discord
from discord.ext import commands


class CustomEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_succesful(self, ctx):
        await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
    async def on_command_failed(self, ctx):
        await ctx.message.add_reaction('❌')


def setup(client):
    client.add_cog(CustomEvents(client))

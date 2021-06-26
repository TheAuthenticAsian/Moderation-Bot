import discord
from discord.ext import commands
from core.server_config import server_config


class CommandLogger(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.log_channel = server_config["log_channel"]

    @commands.Cog.listener()
    async def on_command_successful(self, ctx, successful_embed):
        channel = self.client.get_channel(self.log_channel)
        await channel.send(embed=successful_embed)
        await ctx.send(embed=successful_embed)
        await ctx.message.add_reaction('✅')

    @commands.Cog.listener()
    async def on_command_failed(self, ctx, error_embed):
        await ctx.send(embed=error_embed)
        await ctx.message.add_reaction('❌')


def setup(client):
    client.add_cog(CommandLogger(client))

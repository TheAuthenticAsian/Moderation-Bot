import inspect
import io
import textwrap
import traceback
from contextlib import redirect_stdout
import os
import aiohttp
from discord.ext import commands
import discord
from discord.ext import tasks
from datetime import timedelta, datetime
from core.server_config import server_config

channelID = server_config["commands_only_channel"]
MESSAGEC = "Go chit chat somewhere else, this is for commands only."
MESSAGEMASA = "Hey you ||~~short~~|| *I mean* tall mf, go chit chat somewhere you twat."


class CommandsOnly(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 786057630383865858 and not message.author.bot:

            if message.content.startswith('?'):
                pass

            else:
                await message.delete()
                if message.author.id == server_config["masa_id"]:
                    embed = discord.Embed(
                        title="Commands ONLY", description=MESSAGEMASA, color=discord.Colour.red())
                else:
                    embed = discord.Embed(
                        title="Commands ONLY", description=MESSAGEC, color=discord.Colour.red())

                await message.channel.send(message.author.mention, delete_after=5.0)
                await message.channel.send(embed=embed, delete_after=5.0)


def setup(bot):
    bot.add_cog(CommandsOnly(bot))

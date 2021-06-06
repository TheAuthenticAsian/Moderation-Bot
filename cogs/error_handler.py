import discord
from discord.ext import commands
from core import discord_utils as utils


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await utils.send_embed(ctx, "Command Error!", [{"Details": "You have entered an **invalid argument** for the command"}, {"Help": f'Please check "**{self.client.command_prefix}help**" for the correct usage.'}], discord.Colour.red())
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.send_embed(ctx, "Command Error!", [{"Details": 'You are **missing an argument** to that command'}, {"Help": f'Please check "**{self.client.command_prefix}help**" for the correct usage.'}], discord.Colour.red())
            return

        if isinstance(error, commands.MissingPermissions):
            await utils.send_embed(ctx, "Command Error!", [{"Details": "You **cannot access this command**, you are missing permissions."}], discord.Colour.red())
            return

        if isinstance(error, commands.CommandNotFound):
            await utils.send_embed(ctx, "Command Error!", [{"Details": 'That command **does not exist**.'}, {"Help": f'Please check "**{self.client.command_prefix}help**" for help.'}], discord.Colour.red())
            return

        await utils.send_embed(ctx, "Command Error!", [
            {"Details": f"There has been an unkown error: `{error}`"}], discord.Colour.red())


def setup(client):
    client.add_cog(ErrorHandler(client))

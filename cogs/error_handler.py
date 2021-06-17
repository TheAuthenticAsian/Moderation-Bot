import discord
from discord.ext import commands
from core import discord_utils as utils


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await utils.error_embed(ctx, "Command Error!", {"Details": "You have entered an **invalid argument** for the command", "Help": f'Please check "**{self.client.command_prefix}help**" for the correct usage.'})
            return
        if isinstance(error, commands.MissingRequiredArgument):
            await utils.error_embed(ctx, "Command Error!", {"Details": 'You are **missing an argument** to that command', "Help": f'Please check "**{self.client.command_prefix}help**" for the correct usage.'})
            return

        if isinstance(error, commands.MissingPermissions):
            await utils.error_embed(ctx, "Command Error!", {"Details": "You **cannot access this command**, you are missing permissions."})
            return

        if isinstance(error, commands.CommandNotFound):
            await utils.error_embed(ctx, "Command Error!", {"Details": 'That command **does not exist**.', "Help": f'Please check "**{self.client.command_prefix}help**" for help.'})
            return

        await utils.error_embed(ctx, "Command Error!",
                                {"Details": f"There has been an unknown error: `{error}`"})


def setup(client):
    client.add_cog(ErrorHandler(client))

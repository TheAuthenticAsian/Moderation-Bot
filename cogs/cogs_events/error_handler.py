import discord
from discord.ext import commands
from core.utils import embed_utils as utils


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        error_embed = None

        if isinstance(error, commands.BadArgument):
            error_embed = utils.error_embed("Command Error!", {
                "Details": "You have entered an **invalid argument** for the command", "Help": f'Please check "**{self.client.command_prefix}help**" for the correct usage.'})
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed = utils.error_embed("Command Error!", {
                "Details": 'You are **missing an argument** to that command', "Help": f'Please check "**{self.client.command_prefix}help**" for the correct usage.'})

        if isinstance(error, commands.MissingPermissions):
            error_embed = utils.error_embed("Command Error!", {
                "Details": "You **cannot access this command**, you are missing permissions."})

        if isinstance(error, commands.CommandNotFound):
            error_embed = utils.error_embed("Command Error!", {
                "Details": 'That command **does not exist**.', "Help": f'Please check "**{self.client.command_prefix}help**" for help.'})

        if error_embed is None:
            error_embed = utils.error_embed("Command Error!",
                                            {"Details": f"There has been an unknown error: `{error}`"})
        self.client.dispatch("command_failed", ctx, error_embed)


def setup(client):
    client.add_cog(ErrorHandler(client))

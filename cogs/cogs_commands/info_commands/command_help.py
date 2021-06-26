import operator
import discord
from discord.ext import commands
from core import embed_utils as utils


class Helper(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

        # Sort the commands from least to greatest so it's more aesthetic
        self.command_list = list(self.client.commands)
        self.command_list.sort(reverse=True,
                               key=lambda x: -len(operator.attrgetter('description')(x)))

    @commands.command(description="The help command.")
    async def help(self, ctx, command_name=None):
        # Find the help section of the requested command and if not found, say it doesn't exist.
        if command_name is not None:
            requested_command = None
            for command in self.command_list:
                if command_name == command.name:
                    requested_command = command
                    break
            if not requested_command:
                error_embed = utils.error_embed("Help Command Error!",
                                                {"Details": "That command name does not exist. Use #help for the available commands."})
                self.client.dispatch("command_failed", ctx, error_embed)
                return

            command_index = self.command_list.index(requested_command)
            command = self.command_list[command_index]

            help_embed = utils.create_base_embed(f'Command: "{command}"', [
                {"Description": f'`{command.description}`'}, {'Usage': f'`{self.client.command_prefix}{command.help}`'}], discord.Colour.red())
            await ctx.send(embed=help_embed)
            await ctx.message.add_reaction('✅')

        else:
            command_dict = {}

            for command in self.command_list:
                command_dict[command.name] = f'`{command.description}`'

            help_embed = utils.create_base_embed('Help', [
                command_dict], description='`Use #help (command) to get more information on a command.`')

            await ctx.send(embed=help_embed)

            await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Helper(client))

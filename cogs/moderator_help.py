import operator
import discord
from discord.ext import commands
from core import discord_utils as utils


class Helper(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

        # Sort the commands from least to greatest so it's more aestetic
        self.command_list = [command for command in self.client.commands]
        self.command_list.sort(reverse=True,
                               key=lambda x: -len(operator.attrgetter('description')(x)))

    @commands.command(description="The help command.")
    async def help(self, ctx, command_name=None):
        # Find the help section of the requeted command and if not found, say it doesn't exist.
        if command_name != None:
            requested_command = None
            for command in self.command_list:
                if command_name == command.name:
                    requested_command = command
                    break
            if not requested_command:
                await utils.error_embed(ctx, "Help Command Error!",
                                        {"Details": "That command name does not exist. Use #help for the available commands."})
                self.client.dispatch("command_failed", ctx)
                return

            command_index = self.command_list.index(requested_command)
            command = self.command_list[command_index]

            await utils.send_embed(ctx, f'Command: "{command}"', [
                {"Description": f'`{command.description}`'}, {'Usage': f'`{self.client.command_prefix}{command.help}`'}], discord.Colour.red())
            self.client.dispatch("command_succesful", ctx)

        else:
            command_dict = {}

            for command in self.command_list:
                command_dict[command.name] = f'`{command.description}`'

            await utils.send_embed(ctx, f'Help', [command_dict], description='`Use #help (command) to get more information on a command.`')

            self.client.dispatch("command_succesful", ctx)


def setup(client):
    client.add_cog(Helper(client))

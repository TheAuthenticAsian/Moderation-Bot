import discord
from discord.ext import commands
from core import discord_utils as utils
from core import database

# This file is for commands to give user the data, for example to get people that are banned or who kicked who.

# String template for getlist command. 0 = username, 1 = what happenend, 2 = person who did it, 3 = date, 4 = reason
list_template = '**{0}** was {1} by **{2}** on **{3}** for **"{4}"** \n'


class ModeratorData(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    # Get list for the desired database
    @commands.command(name='getdata', description='Returns all of the data in the requested database.')
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def get_data(self, ctx, data_type: str):
        """
        getdata (warned_users, banned_users, or kicked_users)
        """

        # A dictionary to get the correct database for the given input
        data = {"warned_users": database.WarnedUser,
                "banned_users": database.BannedUser, "kicked_users": database.KickedUser}

        text_list = []

        requested_data = data[data_type]

        if not requested_data:
            await utils.error_embed(ctx, "Command Error!", {"Details": 'Invalid Argument: `Please choose either "warned_users", "banned_users", or "kicked_users"`'})
            self.client.dispatch("command_failed", ctx)
            return

        for user_data in requested_data.select():
            text_list.append(list_template.format(
                user_data.username, data_type.split("_")[0], user_data.moderator, user_data.date, user_data.reason))

        if len(text_list) == 0:
            await utils.error_embed(ctx, "Command Error!", {"Details": '`There is no data available for this database.`'})
            self.client.dispatch("command_failed", ctx)
            return

        user_data = await self.client.fetch_user(ctx.author.id)
        await user_data.send(">>> " + ''.join(text_list))
        self.client.dispatch("command_successful", ctx)

    @ commands.command(name='search', description='Returns all of the data in the database for a specific user.')
    @ commands.has_permissions(kick_members=True, ban_members=True)
    async def search(self, ctx, user: discord.Member):
        """
        search (mention user here)
        """
        text_list = []

        # function to add data to the text_list
        def add_to_list(model, text: str):
            data_list = model.select().where(model.user_id == user.id)
            for data in data_list:
                text_list.append(list_template.format(
                    data.username, text, data.moderator, data.date, data.reason))

        add_to_list(database.WarnedUser, "warned")
        add_to_list(database.BannedUser, "banned")
        add_to_list(database.KickedUser, "kicked")

        if len(text_list) == 0:
            await utils.error_embed(ctx, "Command Error!", {"Details": '`There is no data available for this database table.`'})
            self.client.dispatch("command_failed", ctx)
            return

        user = await self.client.fetch_user(ctx.author.id)
        await user.send(">>> " + ''.join(text_list))
        self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(ModeratorData(client))

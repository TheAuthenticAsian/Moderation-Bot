import discord
from discord.ext import commands
from core import discord_utils as utils
from core import database

# Commands to give user the data, for example to get people that are banned or who kicked who.


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
        dataget (warned_users, banned_users, or kicked_users)
        """

        data = {"warned_users": database.WarnedUser,
                "banned_users": database.BannedUser, "warned_users": database.WarnedUser}

        text_list = []

        requested_data = data[data_type]

        if requested_data:
            for user_data in requested_data.select():
                text_list.append(list_template.format(
                    user_data.username, data_type.split("_")[0], user_data.moderator, user_data.date, user_data.reason))
        else:
            await utils.send_embed(ctx, "Command Error!", [{"Details": 'Invalid Argument: `Please choose either "warned_users", "banned_users", or "kicked_users"`'}], discord.Colour.red())
            return

        if len(text_list) == 0:
            await utils.send_embed(ctx, "Command Error!", [{"Details": '`There is no data available for this database table.`'}], discord.Colour.red())
            return

        user_data = await self.client.fetch_user(ctx.author.id)
        await user_data.send(">>> " + '\n'.join(text_list))

    @ commands.command(name='search', description='Returns all of the data in the database for a specific user.')
    @ commands.has_permissions(kick_members=True, ban_members=True)
    async def search(self, ctx, user: discord.User):
        """
        search (mention user here)
        """
        text_list = []

        warned_list = database.WarnedUser.select().where(
            database.WarnedUser.user_id == user.id)
        banned_list = database.BannedUser.select().where(
            database.BannedUser.user_id == user.id)
        kicked_list = database.KickedUser.select().where(
            database.KickedUser.user_id == user.id)

        def add_to_list(text: str, data_list):
            for data in data_list:
                text_list.append(list_template.format(
                    data.username, text, data.moderator, data.date, data.reason))

        add_to_list("warned", warned_list)
        add_to_list("banned", banned_list)
        add_to_list("kicked", kicked_list)

        if len(text_list) == 0:
            await utils.send_embed(ctx, "Command Error!", [{"Details": '`There is no data available for this database table.`'}], discord.Colour.red())
            return

        user = await self.client.fetch_user(ctx.author.id)
        await user.send(">>> " + '\n'.join(text_list))


def setup(client):
    client.add_cog(ModeratorData(client))

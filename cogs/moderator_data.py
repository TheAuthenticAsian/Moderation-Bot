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
    @commands.command(name='dataget', description='Returns all of the data in the requested database.')
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def data_get(self, ctx, data_type: str):
        """
        dataget (warned_users, banned_users, or kicked_users)
        """

        text_list = []

        if data_type == "warned_users":
            warned_list = database.WarnedUser.select()

            for warned_user in warned_list:
                text_list.append(list_template.format(
                    warned_user.username, "warned", warned_user.warned_by, warned_user.date_warned, warned_user.reason))

        elif data_type == "banned_users":
            banned_list = database.BannedUser.select()

            for banned_user in banned_list:
                text_list.append(list_template.format(
                    banned_user.username, "banned", banned_user.banned_by, banned_user.date_banned, banned_user.reason))
        elif data_type == "kicked_users":
            kicked_list = database.KickedUser.select()

            for kicked_user in kicked_list:
                text_list.append(list_template.format(
                    kicked_user.username, "kicked", kicked_user.kicked_by, kicked_user.date_kicked, kicked_user.reason))
        else:
            await utils.send_embed(ctx, "Command Error!", [{"Details": 'Invalid Argument: `Please choose either "warned_users", "banned_users", or "kicked_users"`'}], discord.Colour.red())
            return

        if len(text_list) == 0:
            await utils.send_embed(ctx, "Command Error!", [{"Details": '`There is no data available for this database table.`'}], discord.Colour.red())
            return

        user = await self.client.fetch_user(ctx.author.id)
        await user.send(">>> " + '\n'.join(text_list))

    @commands.command(name='search', description='Returns all of the data in the database for a specific user.')
    @commands.has_permissions(kick_members=True, ban_members=True)
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

        for warned_user in warned_list:
            text_list.append(list_template.format(
                warned_user.username, "warned", warned_user.warned_by, warned_user.date_warned, warned_user.reason))

        for banned_user in banned_list:
            text_list.append(list_template.format(
                banned_user.username, "banned", banned_user.banned_by, banned_user.date_banned, banned_user.reason))

        for kicked_user in kicked_list:
            text_list.append(list_template.format(
                kicked_user.username, "kicked", kicked_user.kicked_by, kicked_user.date_kicked, kicked_user.reason))

        if len(text_list) == 0:
            await utils.send_embed(ctx, "Command Error!", [{"Details": '`There is no data available for this database table.`'}], discord.Colour.red())
            return

        user = await self.client.fetch_user(ctx.author.id)
        await user.send(">>> " + '\n'.join(text_list))


def setup(client):
    client.add_cog(ModeratorData(client))

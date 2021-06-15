import discord
from discord.ext import commands
from core import discord_utils as utils
from core import database
from pygicord import Paginator

# This file is for commands to give user the data, for example to get people that are banned or who kicked who.

# String template for getlist command. 0 = username, 1 = what happenend, 2 = person who did it, 3 = date, 4 = reason
list_template = '**{0}** was {1} by **{2}** on **{3}** for **"{4}"** \n'


class ModeratorData(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    # Get list for the desired database
    @commands.command(name='getdata', description='Returns all of the data in the requested database.')
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def get_data(self, ctx, case_number: int):
        """
        getdata (case_number)
        """

        async def get_pages():
            pages = []
            # Generate a list of 5 embeds
            query = database.ModerationLogs.select().where(
                database.ModerationLogs.id == case_number)

            if query.exists():
                for q in query:
                    modObj = await self.client.fetch_user(q.moderator_id)
                    user = await self.client.fetch_user(q.user_id)

                    embed = discord.Embed(
                        title="Query Results", description=f"Query requested by {ctx.author.mention}.\nSearch Query: {user.mention}")
                    embed.add_field(
                        name="Data", value=f"**User:** {q.username}\n**User ID:** {q.user_id}\n**\n**Moderator** {modObj.display_name}\n**Date:** {str(q.date)}\n**Action:** {q.action}\n**Reason:** {q.reason}\n**")
                    embed.set_footer(text=f"Case ID: {q.id}")

                    pages.append(embed)
                return pages
            else:
                return None

        value = await get_pages()

        if value == None:
            await utils.error_embed(ctx, "Command Error!", {"Details": '`There is no data available for this database table.`'})
            await self.client.dispatch("command_failed", ctx)
            return

        paginator = Paginator(pages=value)
        await paginator.start(ctx)

        await self.client.dispatch("command_successful", ctx)

    @commands.command(name='search', description='Returns all of the data in the database for a specific user.')
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def search(self, ctx, user: discord.Member):
        """
        search (mention user here)
        """

        async def get_pages():
            pages = []
            # Generate a list of 5 embeds
            query = database.ModerationLogs.select().where(
                database.ModerationLogs.user_id == user.id)

            if query.exists():
                for q in query:
                    modObj = await self.client.fetch_user(q.moderator_id)

                    embed = discord.Embed(
                        title="Query Results", description=f"Query requested by {ctx.author.mention}.\nSearch Query: {user.mention}")
                    embed.add_field(
                        name="Data", value=f"**User:** {q.username}\n**User ID:** {q.user_id}\n**\n**Moderator** {modObj.display_name}\n**Date:** {str(q.date)}\n**Action:** {q.action}\n**Reason:** {q.reason}\n**")
                    embed.set_footer(text=f"Case ID: {q.id}")

                    pages.append(embed)
                return pages
            else:
                return None

        value = await get_pages()

        if value == None:
            await utils.error_embed(ctx, "Command Error!", {"Details": '`There is no data available for this database table.`'})
            await self.client.dispatch("command_failed", ctx)
            return

        paginator = Paginator(pages=value)
        await paginator.start(ctx)

        await self.client.dispatch("command_successful", ctx)


def setup(client):
    client.add_cog(ModeratorData(client))

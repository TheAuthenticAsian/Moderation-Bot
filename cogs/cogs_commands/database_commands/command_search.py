import discord
from discord.ext import commands
from core.utils import embed_utils as utils
from core import database
from pygicord import Paginator


# String template for getlist command. 0 = username, 1 = what happenend, 2 = person who did it, 3 = date, 4 = reason
list_template = '**{0}** was {1} by **{2}** on **{3}** for **"{4}"** \n'


class Search(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    # Get list for the desired database
    @commands.command(name='search', description='Returns the data for a specific case id.')
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def search(self, ctx, case_number: int):
        """
        search (case_number)
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

            return None

        value = await get_pages()

        if value is None:
            error_embed = utils.error_embed(
                ctx, "Command Error!", {"Details": '`That case-id does not exist.`'})
            self.client.dispatch("command_failed", ctx, error_embed)
            return

        paginator = Paginator(pages=await get_pages())
        await paginator.start(ctx)

        await ctx.message.add_reaction('✅')


def setup(client):
    client.add_cog(Search(client))

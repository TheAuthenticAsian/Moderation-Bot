import discord
from discord.ext import commands
from core.utils import embed_utils as utils
from core import database


# String template for getlist command. 0 = username, 1 = what happenend, 2 = person who did it, 3 = date, 4 = reason
list_template = '**{0}** was {1} by **{2}** on **{3}** for **"{4}"** \n'


class GetData(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client

    # Get list for the desired database
    @commands.command(name='getdata', description='Returns all of the case_id data in the for the specified user.')
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def getdata(self, ctx, user: discord.Member):
        """
        getdata (mention user here)
        """

        query = database.ModerationLogs.select().where(
            database.ModerationLogs.user_id == user.id)

        if query is None:
            error_embed = utils.error_embed("Command Error!", {
                                            "Details": '`There is no data available for this database table.`'})
            self.client.dispatch("command_failed", ctx, error_embed)
            return

        send_value = []

        for q in query:
            modObj = await self.client.fetch_user(q.moderator_id)
            send_value.append(
                f"`**{q.id}**` **[{q.action}]** `**{q.date}**`")

        send_value = "\n".join(send_value)

        embed = discord.Embed(
            title="Data Request")
        embed.add_field(name="Data",
                        value=send_value)
        embed.set_footer(
            text=f"Query requested by {ctx.author}.\nSearch Query: {user}")

        self.client.dispatch("command_successful", ctx, embed)


def setup(client):
    client.add_cog(GetData(client))

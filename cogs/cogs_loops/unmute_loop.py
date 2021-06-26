from discord.ext import commands
import discord
from core import database
from datetime import datetime
from core import discord_utils as utils
from discord.ext import tasks
from core.server_config import server_config


class UnMuteLoop(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
        self.guild_id = server_config["guild_id"]
        self.log_channel = server_config["log_channel"]
        self.unmute_loop.start()

    @tasks.loop(seconds=60)
    async def unmute_loop(self):
        timestamp = datetime.now()
        current_time = timestamp.strftime(r'%m/%d, %H:%M')

        muted_users = database.MutedUser.select().where(
            (database.MutedUser.mute_time_release <= current_time))

        if muted_users:
            for user in muted_users:
                guild: discord.Guild = self.client.get_guild(self.guild_id)
                guild_member = guild.get_member(user.user_id)
                muted_role = discord.utils.get(guild.roles, name='Muted')
                await guild_member.remove_roles(muted_role)
                await utils.successful_embed(self.client.get_channel(self.log_channel), "Unmute Results", guild_member, self.client.user, {"Details": f'{guild_member.mention} has been umuted'})
                user.delete_instance()

    @unmute_loop.before_loop
    async def before_unmute_loop(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(UnMuteLoop(client))

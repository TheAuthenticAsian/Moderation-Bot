import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# enviroment thing
load_dotenv()

bot_token = os.getenv('token')
bot_prefix = "??"

cogs_folder = "./cogs"

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.presences = True
intents.bans = True

client = commands.Bot(command_prefix=bot_prefix,
                      help_command=None, intents=intents)


# set activity
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{bot_prefix}help"))

# load cogs
for file in os.listdir(cogs_folder):
    if file.endswith(".py"):
        try:
            client.load_extension(f"cogs.{file[:-3]}")
            print(f"Loaded: {file}")
        except Exception as e:
            print(f"Could not load: {file}")
            print(e)


client.run(bot_token)

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time

start_time = time.time()

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


def load_cog_files(folder: str):
    """[Load Cogs Recursively]

    Args:
        folder (str): [Folder Path]
    """

    # We don't want to load pycache folder if there is one
    if folder.find("__pycache__") != -1:
        return

    extension_name = folder.replace("/", ".")[2:]

    for file in os.listdir(folder):
        # delete the first two characters because they're ".." because of the replace method

        if file.endswith(".py"):
            try:
                client.load_extension(f"{extension_name}.{file[:-3]}")
                print(f"Loaded: {file}")
            except Exception as e:
                print(f"Could not load: {file}")
                print(e)
            continue

        if os.path.isdir(f"{folder}/{file}"):
            load_cog_files(f"{folder}/{file}")


load_cog_files(cogs_folder)

print("My program took", time.time() - start_time, "to run")

client.run(bot_token)

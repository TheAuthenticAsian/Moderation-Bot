import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# enviroment thing
load_dotenv()

BOT_TOKEN = os.getenv('token')
BOT_PREFIX = "??"

COGS_FOLDER = "./cogs"

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.presences = True
intents.bans = True

client = commands.Bot(command_prefix=BOT_PREFIX,
                      help_command=None, intents=intents)


# set activity
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"{BOT_PREFIX}help"))

# load cogs


def load_cog_files(folder: str):
    """[Load Cogs Recursively]

    Args:
        folder (str): [Folder Path]
    """

    # We don't want to load pycache folder if there is one
    if folder.find("__pycache__") != -1:
        return

    # delete the first two characters because they're ".." because of the replace method
    extension_name = folder.replace("/", ".")[2:]

    for file in os.listdir(folder):

        if file.endswith(".py"):
            try:
                client.load_extension(f"{extension_name}.{file[:-3]}")
                print(f"Loaded: {file}")
            except Exception as error:
                print(f"Could not load: {file}")
                print(error)
            continue

        if os.path.isdir(f"{folder}/{file}"):
            load_cog_files(f"{folder}/{file}")


load_cog_files(COGS_FOLDER)
client.run(BOT_TOKEN)

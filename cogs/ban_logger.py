import discord
from discord.ext import commands
from random import randint
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import re
from datetime import datetime

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("SchoolSimplifiedBans").sheet1


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


class BanUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        now = datetime.now()
        '''
		Discord.py doesn't give us the information we need so we need to dig deeper and query the audit logs
		'''

        async for logs in guild.audit_logs(limit=1, oldest_first=False, action=discord.AuditLogAction.ban):
            # Query the audit log for a type ban, user, and get the latest one.

            #logs = logs[0]
            # Getting the first entry in the list. Theres only 1 in there anywayimport discord

            '''
            Okay so now we fetched everything, now we need to access the attributes from 'logs'.
            '''

            moderator = logs.user
            target = logs.target

            # We need to check who banned the person.
            if moderator.id == 536991182035746816:  # Wick's ID
                banReasonAUDIT = logs.reason

                banReason = re.match(
                    r"[^[]*\[([^]]*)\]", banReasonAUDIT).groups()[0]
                random, fullUsernameMOD = banReasonAUDIT.split("- ")

            else:
                banReason = logs.reason
                # Get full username with tag
                fullUsernameMOD = f"{moderator.display_name}#{moderator.discriminator}"

            # Okay now we got our reason, we need to get a few more things

            timestamp = now.strftime(
                "%m/%d/%Y %H-%M-%S")  # Get our timestamp

            # Get full username with tag
            fullUsernameTARGET = f"{target.display_name}#{target.discriminator}"

            # Get everything into a list so we can bulk insert.
            row = [timestamp, fullUsernameTARGET, "", str(
                target.id), "", fullUsernameMOD, "", banReason]
            # next_row = next_available_row(sheet) #Find a row

            sheet.insert_row(row, 2)  # Insert data, and boom. We done!
            break


def setup(bot):
    bot.add_cog(BanUpdate(bot))

import discord
import database
from typing import List


def create_embed(name: str, field_table: List[dict], color: discord.Colour = discord.Colour.blue(), description="", thumbnail=None):
    embed = discord.Embed(title=name, description=description, color=color)

    for field_dict in field_table:
        for field in field_dict:
            embed.add_field(
                name=field, value=field_dict[field], inline=False)

    embed.set_footer(text='"Masa is ||~short~||" - ChilledFrost')

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    return embed


def successful_embed(name: str, user, moderator: str, details: dict, reason=None):
    if not user:
        return create_embed(name, [{"🚓 Moderator": moderator}, details])

    user_data = database.ModerationLogs.select().where(
        database.ModerationLogs.reason == reason)
    case_id = None
    if user_data.exists():
        case_id = user_data[0].id

    if case_id:
        if not reason:
            return create_embed(name, [{"👤 User": user}, {"🚓 Moderator": moderator}, details, {"Case-ID": case_id}], thumbnail=user.avatar_url)

        return create_embed(name, [{"👤 User": user}, {"📝 Reason": reason}, {"🚓 Moderator": moderator}, details, {"Case-ID": case_id}], thumbnail=user.avatar_url)

    if not reason:
        return create_embed(name, [{"👤 User": user}, {"🚓 Moderator": moderator}, details], thumbnail=user.avatar_url)

    return create_embed(name, [{"👤 User": user}, {"📝 Reason": reason}, {"🚓 Moderator": moderator}, details], thumbnail=user.avatar_url)


def error_embed(error_message: str, details: dict):
    return create_embed(error_message, [details], color=discord.Colour.red())

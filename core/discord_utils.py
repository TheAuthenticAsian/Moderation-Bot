from datetime import datetime, timedelta
from typing import List
import discord


async def send_embed(ctxs, name: str, field_table: List[dict], color: discord.Colour = discord.Colour.blue(), description="", thumbnail=None):
    """[Make sending an embed easier and more quicker]

    Args:
        ctx ([Context]): [The context]
        name (str): [The title of the embed]
        field_table (List[dict]): [A table containing dictionaries, the key of which is name of the field, and the value is the value of the field]
        color ([discord.Colour], optional): [The color you want]. Defaults to discord.Colour.blue().
        description (str, optional): [The description]. Defaults to "".
    """
    embed = discord.Embed(title=name, description=description, color=color)

    for field_dict in field_table:
        for field in field_dict:
            embed.add_field(
                name=field, value=field_dict[field], inline=False)

    embed.set_footer(text='"Masa is ||~short~||" - ChilledFrost')

    if thumbnail:
        embed.set_thumbnail(url=thumbnail)

    print(ctxs)

    for ctx in ctxs:
        await ctx.send(embed=embed)


async def successful_embed(ctx, name: str, user, moderator: str, details: dict, reason=None):
    """[Send an embed saying the command was successful]

    Args:
        ctx ([Context]): [The ctx]
        name (str): [The name of the embed]
        user ([type]): [The user]
        moderator (str): [The moderator]
        details (dict): [details (dict): [A dictionary, the key is the title, and the value is the message]
        reason ([type], optional): [The reason]. Defaults to None.
    """
    if not user:
        await send_embed(ctx, name, [{"🚓 Moderator": moderator}, details])
        return

    if not reason:
        await send_embed(ctx, name, [{"👤 User": user}, {"🚓 Moderator": moderator}, details], thumbnail=user.avatar_url)
        return

    await send_embed(ctx, name, [{"👤 User": user}, {"📝 Reason": reason}, {"🚓 Moderator": moderator}, details], thumbnail=user.avatar_url)


async def error_embed(ctx, error_message: str, details: dict):
    """[Send an error embed]

    Args:
        ctx ([Context]): [The discord context]
        error_message (str): [The title of the embed]
        details (dict): [A dictionary, the key is the title, and the value is the message]
    """
    await send_embed([ctx], error_message, [details], color=discord.Colour.red())


def convert_time_to_seconds(time):
    time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        return int(time[:-1]) * time_convert[time[-1]]
    except:
        return time


def showFutureTime(time):
    now = datetime.now()
    output = convert_time_to_seconds(time)

    add = timedelta(seconds=int(output))
    now_plus_10 = now + add

    return now_plus_10.strftime(r'%m/%d, %H:%M')

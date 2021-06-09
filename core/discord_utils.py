import discord


async def send_embed(ctx, name, field_table, color=discord.Colour.blue(), description=""):
    embed = discord.Embed(title=name, description=description, color=color)

    for field_dict in field_table:
        for field in field_dict:
            embed.add_field(
                name=field, value=field_dict[field], inline=False)

    embed.set_footer(text='"Masa is ||~short~||" - ChilledFrost')

    await ctx.send(embed=embed)


async def sucessful_embed(ctx, name: str, user, moderator: str, details: dict, reason=None,):
    """[Send an embed saying the command was sucessful]

    Args:
        ctx ([Context]): [The ctx]
        name (str): [The name of the embed]
        user ([type]): [The user]
        moderator (str): [The moderator]
        details (dict): [details (dict): [A dictionary, the key is the title, and the value is the message]
        reason ([type], optional): [The reason]. Defaults to None.
    """
    if not reason:
        await send_embed(ctx, name, [{"👤 User": user}, {"🚓 Moderator": moderator}, details])
        return

    await send_embed(ctx, name, [{"👤 User": user}, {"📝 Reason": reason}, {"🚓 Moderator": moderator}, details])


async def error_embed(ctx, error_message: str, details: dict):
    """[Send an error embed]

    Args:
        ctx ([Context]): [The discord context]
        error_message (str): [The title of the embed]
        details (dict): [A dictionary, the key is the title, and the value is the message]
    """
    await send_embed(ctx, error_message, [details], color=discord.Colour.red())

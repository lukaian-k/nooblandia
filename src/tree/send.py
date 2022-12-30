import discord
from discord import app_commands


async def fn_send(interaction:discord.Interaction, client, channel:str, message:str):
    channel = int(channel)
    channel = client.get_channel(channel)

    await channel.send(message)
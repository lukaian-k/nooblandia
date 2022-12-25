import discord

from src.system.json import *
from src.system.directories import *
from src.system.ready import *

from src.reply.defaults import *


BOT = dict(read_json(DIR_SECRET))
intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    await ready(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await defaults(message)


client.run(BOT["TOKEN"])

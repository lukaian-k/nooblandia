import discord
import json

from src.system.json import *
from src.system.directories import *
from src.system.ready import *

from src.reply.defaults import *

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


bot = dict(read_json(DIR_SECRET))
client.run(bot["TOKEN"])

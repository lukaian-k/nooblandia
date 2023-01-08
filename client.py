import discord

from database.directories import *

from src.system.json import *
from src.system.ready import *

from src.reply.defaults import *


BOT = dict(
    read_json(DIR_SECRET["BOT"])
)

class Client(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)

    async def on_ready(self):
        await self.wait_until_ready()
        await ready(self)

client = Client(
    intents=discord.Intents.all()
)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await defaults(message)


client.run(BOT["TOKEN"])
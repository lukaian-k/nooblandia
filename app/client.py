import discord
from discord import app_commands

from src.system.json import *
from src.system.ready import *
from src.system.directories import *

from src.reply.defaults import *


BOT = dict(read_json(DIR_SECRET))

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            self.synced = True

        await ready(self)

client = Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await defaults(message)


client.run(BOT["TOKEN"])

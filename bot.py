import discord
from discord.ext import commands

import os
import aiohttp

from database.directories import *

from src.system.json import *


BOT = dict(
    read_json(DIR_SECRET["BOT"])
)

class Bot(commands.Bot):
    def __init__(self, command_prefix, intents, application_id):
        super().__init__(
            application_id=application_id,
            command_prefix=command_prefix,
            intents=intents,

            case_insensitive=True,
            help_command=None
        )
        self.synced = False


    async def setup_hook(self):
        self.session = aiohttp.ClientSession()

        for filename in os.listdir('src/cogs'):
            if filename.endswith('.py'):
                print(f"cog add: {filename[:-3]}")
                await bot.load_extension(f'src.cogs.{filename[:-3]}')

        await bot.tree.sync()

    
    async def close(self):
        await super().close()
        await self.session.close()


    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            self.synced = True

        print(f'\nbot.py: ON\n{self.user} connected!')


bot = Bot(
    command_prefix=BOT["command_prefix"],
    intents=discord.Intents.all(),
    application_id=BOT["APP_ID"]
)
bot.run(BOT["TOKEN"])
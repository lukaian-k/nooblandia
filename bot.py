import discord
from discord.ext import commands

import os
import aiohttp

from database.directories import *
from src.system.json import *

from src.system.ready import *


BOT = dict(
    read_json(DIR_SECRET["BOT"])
)

class Bot(commands.Bot):
    def __init__(self, command_prefix, intents, application_id) -> None:
        super().__init__(
            application_id=application_id,
            command_prefix=command_prefix,
            intents=intents,

            case_insensitive=True,
            help_command=None
        )
        self.synced = False


    async def setup_hook(self) -> None:
        self.session = aiohttp.ClientSession()

        DIR_COG = 'src/cogs'
        
        for directory in os.listdir(DIR_COG):
            if directory == '__pycache__':
                continue

            print(f'\nDirectory: {directory}')
            
            for filename in os.listdir(f'{DIR_COG}/{directory}'):
                if filename.endswith('.py'):
                    await self.load_extension(f'src.cogs.{directory}.{filename[:-3]}')
                    print(f'└── Cog added: {filename[:-3]}')

        await bot.tree.sync()

    
    async def close(self) -> None:
        await super().close()
        await self.session.close()


    async def on_command_error(self, ctx, error) -> None:
        embed = discord.Embed(
            colour = 10038562,
            title=error
        )
        await ctx.reply(
            embed=embed,
            ephemeral=True,
            delete_after=20
        )


    async def on_ready(self) -> None:
        await self.wait_until_ready()

        if not self.synced:
            self.synced = True

        await ready(self)


bot = Bot(
    command_prefix=BOT["command_prefix"],
    intents=discord.Intents.all(),
    application_id=BOT["APP_ID"]
)
bot.run(BOT["TOKEN"])
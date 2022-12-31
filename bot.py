import discord
from discord.ext import commands

import os
import asyncio

from numpy import number
from googlesearch import search

from database.directories import *

from src.system.json import *


BOT = dict(read_json(DIR_SECRET))

class Bot(commands.Bot):
    def __init__(self, command_prefix):
        intents = discord.Intents.all()

        super().__init__(
            command_prefix=command_prefix,
            case_insensitive=True,
            intents=intents,
            help_command=None
        )
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            self.synced = True

        print("\nbot.py: ON\n")

bot = Bot(
    BOT["command_prefix"]
)


async def load():
    for filename in os.listdir('src/cogs'):
        if filename.endswith('.py'):
            print(f"cog add: {filename[:-3]}")
            await bot.load_extension(f'src.cogs.{filename[:-3]}')

async def main(TOKEN):
    await load()
    await bot.start(TOKEN)

asyncio.run(
    main(BOT["TOKEN"])
)


# @bot.command(name='google', help='Pesquise rápido no google pelo discord!', aliases=['g','pesquise'])
# async def google(ctx, *args):
#     await ctx.send(f'Aqui estão alguns dos resultados encontrados para "{" ".join(args)}":')
#     for i in set(list(search(' '.join(args), num_results=5, lang="br"))):
#         print(await ctx.send(str(i)))
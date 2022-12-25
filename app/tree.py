import discord
from discord import app_commands

from src.system.json import *
from src.system.directories import *


BOT = dict(read_json(DIR_SECRET))

class Tree(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            await tree.sync()
            self.synced = True

_tree_ = Tree()
tree = app_commands.CommandTree(_tree_)


@tree.command(name='piada', description='Conta piadas')
async def piada(interaction: discord.Interaction):
    await interaction.response.send_message(f"Sou nem palhaça!", ephemeral=True)


_tree_.run(BOT["TOKEN"])
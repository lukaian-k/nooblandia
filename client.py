import discord
from discord import app_commands

from database.directories import *

from src.system.json import *
from src.system.ready import *

from src.reply.defaults import *

from src.tree.imc import *
from src.tree.ship import *
from src.tree.google import *


BOT = dict(read_json(DIR_SECRET))

class Client(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            await tree.sync()
            self.synced = True

        await ready(self)

client = Client()
tree = app_commands.CommandTree(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await defaults(message)


@tree.command(name='imc', description='Calculadora de imc.')
@app_commands.describe(
    peso="Insira o seu Peso.",
    altura="Insira a sua Altura.",
)
async def imc(interaction:discord.Interaction, peso:float, altura:float):
    await fn_imc(interaction, peso, altura)


@tree.command(name='ship', description='Qual será as chances de termos um casalzão 20 por aqui?!')
@app_commands.describe(
    primeira="Marque a primeira pessoa...",
    segunda="Marque a segunda pessoa...",
)
async def ship(interaction:discord.Interaction, primeira:discord.User, segunda:discord.User):
    await fn_ship(interaction, primeira, segunda)


@tree.command(name='google', description='Pesquise rápido no google pelo discord!')
@app_commands.describe(
    buscar="O que deseja buscar?",
)
async def google(interaction:discord.Interaction, buscar:str):
    await fn_google(interaction, buscar)


client.run(BOT["TOKEN"])

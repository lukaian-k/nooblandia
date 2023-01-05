import discord
from discord import app_commands

from importlib import import_module

from database.directories import *

from src.system.json import *
from src.system.ready import *

from src.reply.defaults import *

def module(name):
    DIR_MODULE = 'src.tree.' + name
    return import_module(DIR_MODULE)


BOT = dict(
    read_json(DIR_SECRET["BOT"])
)

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
    await module('imc').imc(interaction, peso, altura)


@tree.command(name='ship', description='Qual será as chances de termos um casalzão 20 por aqui?!')
@app_commands.describe(
    primeira="Marque a primeira pessoa...",
    segunda="Marque a segunda pessoa...",
)
async def ship(interaction:discord.Interaction, primeira:discord.User, segunda:discord.User):
    await module('ship').ship(interaction, primeira, segunda)


@tree.command(name='google', description='Pesquise rápido no google pelo discord!')
@app_commands.describe(
    buscar="O que deseja buscar?",
)
async def google(interaction:discord.Interaction, buscar:str):
    await module('google').google(interaction, buscar)

    
@tree.command(name='rolar_dados', description='Simula uma jogada de dado.')
@app_commands.describe(
    quantos_dados="Quantidade de dados a serem rolados.",
    lados="Quantos lados o dado terá.",
)
async def rolar_dados(interaction:discord.Interaction, quantos_dados:int, lados:int):
    await module('dice').dice(interaction, quantos_dados, lados)


@tree.command(name='chat_gpt', description='Use o poder da AI do OpenAI aqui pelo discord!')
@app_commands.describe(
    prompt="Escreva QUASE tudo quiser, e a Inteligencia Artificial irá te responder!",
)
async def chatGPT(interaction:discord.Interaction, prompt:str):
    await module('chat_gpt').chatGPT(interaction, prompt)


client.run(BOT["TOKEN"])
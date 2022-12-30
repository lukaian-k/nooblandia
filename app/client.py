import discord
from discord import app_commands

from src.system.json import *
from src.system.directories import *
from src.system.ready import *

from src.reply.defaults import *

from src.tree.imc import *
from src.tree.ship import *
from src.tree.send import *


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


@tree.command(name='send', description='Envie mensagens com o bot (uso restrito a admins)')
@app_commands.describe(
    channel="Canal onde deseja enviar a mensagem.",
    message="Mensagem que deseja enviar.",
)
async def send(interaction:discord.Interaction, channel:str, message:str):
    await fn_send(interaction, client, channel, message)


client.run(BOT["TOKEN"])

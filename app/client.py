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
    peso = "Peso da Pessoa.",
    altura = "Altura da Pessoa.",
)
async def imc(interaction: discord.Interaction, peso:float, altura:float):
    result = peso/(altura*altura)
    message = f"\n\nEsse foi o resultado do seu IMC: {result}\nSe você estiver abaixo ou acima do peso normal, procure um médico!"
    
    reply = interaction.response
    
    if (result >= 18.5 and result <= 24.9): await reply.send_message(
        f"Seu estado atual é: Peso Normal {message}"
    )
    elif (result >= 25 and result <= 29.9): await reply.send_message(
        f"Seu estado atual é: Sobrepeso {message}"
    )
    elif (result >= 30 and result <= 34.9): await reply.send_message(
        f"Seu estado atual é: Obesidade I {message}"
    )
    elif (result >= 35 and result <= 39.9): await reply.send_message(
        f"Seu estado atual é: Obesidade II {message}"
    )
    elif (result >= 40 and result <= 49.9): await reply.send_message(
        f"Seu estado atual é: Obesidade III {message}"
    )
    elif (result >= 50): await reply.send_message(
        f"Seu estado atual é: Obesidade IV {message}"
    )
    elif (result < 18.5): await reply.send_message(
        f"Seu estado atual é: Abaixo do peso {message}"
    )


client.run(BOT["TOKEN"])

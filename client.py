import discord
from discord import app_commands

from pprint import pprint

from database.directories import *
from src.system.json import *

from src.system.ready import *

from src.reply.defaults import *


BOT = dict(
    read_json(DIR_SECRET["BOT"])
)
GUILDS_ID = dict(
    read_json(DIR_GUILDS)
)

class Client(discord.Client):
    def __init__(self, intents) -> None:
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        await self.wait_until_ready()

        for i, guild in enumerate(GUILDS_ID):
          await tree.sync(
            guild=discord.Object(id=GUILDS_ID[guild])
          )
          print(f'{i}・{guild}: sync')

        await ready(self)

client = Client(
    intents=discord.Intents.all()
)
tree = app_commands.CommandTree(client)


@client.event
async def on_message(message) -> None:
  if message.author == client.user:
      return

  await defaults(message)


@tree.context_menu(
  name='info',
  guilds=[
    discord.Object(
      id=GUILDS_ID[guild]
    )

    for guild in GUILDS_ID
  ]
)
async def info(interaction:discord.Interaction, message:discord.Message) -> None:
  pprint(message)
  
  reply = interaction.response
  author = message.author

  embed = discord.Embed(
    colour=15277667,
    title='➭ **Informações do Usuário**',
    description=
f'''
**ID:** {author.id}
**Nome:** {author.name}
**Discriminador:** {author.discriminator}
**Nick:** {author.nick if author.nick != None else 'Não tem'}
**Bot:** {'Sim' if author.bot == True else 'Não'}
'''
  )
  embed.set_thumbnail(url=author.avatar.url)
  await reply.send_message(embed=embed)


client.run(BOT["TOKEN"])
import discord
from discord import app_commands

import openai

from database.directories import *
from src.system.json import *


async def chatGPT(interaction:discord.Interaction, prompt:str):
    MODEL = 'text-davinci-003'
    TEMPERATURE = 0.6
    MAX_TOKENS = 150
    
    BOT = dict(
        read_json(DIR_SECRET["SYSTEM"])
    )
    openai.api_key = BOT["OPENAI_API_KEY"]

    response = openai.Completion.create(
        model=MODEL,
        prompt=prompt,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,

        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    output = response["choices"][0]["text"]
    text = "".join(output)


    embed = discord.Embed(
        colour=3426654,
        title='chatGPT 🤖',
        description=f'**Pergunta:** {prompt}'
    )
    embed.add_field(
        name='➭ Resposta',
        value=text,
        inline=False
    )
    reply = interaction.response
    await reply.send_message(embed=embed)
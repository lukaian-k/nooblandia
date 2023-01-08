import discord
from discord.ext import commands
from discord import app_commands

from googlesearch import search

import openai
from pprint import pprint

from database.directories import *
from src.system.json import *


class Searches(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name='google',
        description='Pesquise rápido no google pelo discord!'
    )
    @app_commands.describe(
        buscar="O que deseja buscar?",
    )
    async def google(self, interaction:discord.Interaction, buscar:str) -> None:
        print(f'\nBusca Por: {buscar}\n')

        found = list(
            set(
                search(
                    buscar,
                    num_results=5,
                    lang="br"
                )
            )
        )

        icon = "➭ "
        found = icon + f'\n\n{icon}'.join(found)

        print(found)

        embed = discord.Embed(
            colour = 1146986,
        
            title = f'Aqui estão alguns dos resultados encontrados para ({buscar}):',
            description = f'**{found}**'
        )

        reply = interaction.response

        await reply.send_message(
            ephemeral=True,
            embed=embed
        )
    

    @app_commands.command(
        name='chat_gpt',
        description='Use o poder da AI do OpenAI aqui pelo discord!'
    )
    @app_commands.describe(
        prompt="Escreva QUASE tudo quiser, e a Inteligencia Artificial irá te responder!",
    )
    async def chatGPT(self, interaction:discord.Interaction, prompt:str) -> None:
        try:
            await interaction.response.defer()

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


            output = response["choices"][0]["text"]; pprint(output)
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
            await interaction.edit_original_response(embed=embed)

        except Exception as error:
            print(error)


async def setup(bot) -> None:
    await bot.add_cog(
        Searches(bot)
    )
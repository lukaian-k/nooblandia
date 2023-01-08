import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

from youtube_dl import YoutubeDL

import openai
from pprint import pprint

from src.system.system import clear_dir

from database.directories import *
from src.system.json import *


class Features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name='download',
        description='Faz download de videos do YouTube apartir de links.'
    )
    @app_commands.describe(
        link="Link do vídeo do YouTube que deseja baixar!",
        ext="Formato do Arquivo.",
    )
    @app_commands.choices(
        ext = [
            Choice(
                name='Vídeo ➭ mp4',
                value='mp4'
            ),
            Choice(
                name='Vídeo ➭ mov',
                value='mov'
            ),
            Choice(
                name='Vídeo ➭ mkv',
                value='mkv'
            ),
            Choice(
                name='Áudio ➭ mp3',
                value='mp3'
            ),
            Choice(
                name='Áudio ➭ wav',
                value='wav'
            ),
            Choice(
                name='Áudio ➭ ogg',
                value='ogg'
            )
        ]
    )
    async def download(self, interaction:discord.Interaction, link:str, ext:str) -> None:
        await interaction.response.defer()

        ydl_opts = {
            "format": f'bestvideo[ext={ext}]+bestaudio[ext=m4a]/best[ext={ext}]/best',
            "outtmpl": f'assets/downloads/temp.{ext}',
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                link = [link.strip()]
                ydl.download(link)

                embed = discord.Embed(
                    colour = 5763719,
                    title = 'Download Concluido!',
                    description = '➭ Aqui está o **seu pedido**!'
                )

                with open(ydl_opts["outtmpl"], 'rb') as file:
                    user = interaction.user
                    file = discord.File(file, filename=f'pedido_de_{user}.{ext}')

                    await interaction.edit_original_response(
                        attachments=[file],
                        embed=embed
                    )
                    
            except Exception as error:
                print(error)
                
                embed = discord.Embed(
                    colour = 15548997,
                    title = 'Algo deu errado!',
                    description = 'Não foi possível **baixar ou enviar** o vídeo'
                )
                await interaction.edit_original_response(embed=embed)

        clear_dir('assets/downloads')


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


async def setup(bot):
    await bot.add_cog(
        Features(bot)
    )
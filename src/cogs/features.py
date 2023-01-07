import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

import openai
from pprint import pprint

from src.system.system import clear_dir

from database.directories import *
from src.system.json import *


class Features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='download',
        help='Faz download de videos do YouTube apartir de links.',
        aliases=["d","baixar"],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def download(self, ctx, link:str, ext:str) -> None:
        ydl_opts = {
            "format": f'bestvideo[ext={ext}]+bestaudio[ext=m4a]/best[ext={ext}]/best',
            "outtmpl": f'assets/downloads/temp.{ext}',
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                embed = discord.Embed(
                    colour = 5793266,

                    title = '➭ Tudo Certo!',
                    description = 'Apenas aguarde o download ser concluido...'
                )
                await ctx.reply(embed=embed)

                link = [link.strip()]
                ydl.download(link)

                embed.colour = 5763719
                embed.title = 'Download Concluido!'
                embed.description = '➭ Aqui está o **seu pedido**!'

                with open(ydl_opts["outtmpl"], 'rb') as file:
                    await ctx.reply(
                        file=discord.File(file),
                        embed=embed
                    )
            except:
                embed = discord.Embed(
                    colour = 15548997,
                    title = 'Algo deu errado!',
                    description = 'Não foi possível **baixar ou enviar** o vídeo'
                )
                await ctx.reply(embed=embed)

        clear_dir('assets/downloads')


    @commands.command(
        name='chat_gpt',
        help='Use o poder da AI do OpenAI aqui pelo discord!',
        aliases=["chat","gpt","cg"],
    )
    async def chatGPT(self, ctx, *prompt) -> None:
        prompt = " ".join(prompt)
        
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
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Features(bot))
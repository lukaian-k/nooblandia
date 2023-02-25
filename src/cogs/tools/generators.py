import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

from random import sample
import pyshorteners

import openai, os
from dotenv import load_dotenv
from pprint import pprint

from database.directories import *
from src.system.json import *


class Generators(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(
        name='password_generator',
        help='Gera senhas aleatorias para você.',
        aliases=["password","gs","senha","gerar_senha"],
    )
    async def password_generator(self, ctx, size:int=16) -> None:
        try:
            caracters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()!"
            password = "".join(sample(caracters, size))

            embed = discord.Embed(
                colour = 3447003,

                title = 'Aqui está a sua senha!',
                description = f'➭ Senha gerada: **{password}**'
            )
            await ctx.author.send(embed=embed)
            
            embed.colour = 15418782
            embed.title = 'Sua senha foi lhe informada no privado!'
            embed.description = None
            await ctx.reply(embed=embed)
            
        except discord.errors.Forbidden:
            embed = discord.Embed(
                colour = 10038562,
                title = 'Infelizmente não consigo lhe enviar mensagens privadas!',
            )
            await ctx.send(embed=embed)


    @commands.hybrid_command(
        with_app_command=True,

        name='shortlink',
        description='Encurta links para você!',

        help='Encurta links para você!',
        aliases=["short","encurtar"],
    )
    async def shortlink(self, ctx:commands.Context, *,link:str) -> None:
        short = pyshorteners.Shortener().tinyurl.short(link)
        
        embed = discord.Embed(
            colour = 3447003,

            title = 'Link Encurtado!',
            description = f'➭ **{short}**'
        )
        await ctx.reply(embed=embed)


    @app_commands.command(
        name='imagine',
        description='Crie suas imagens usando o poder da AI do OpenAI aqui pelo discord!'
    )
    @app_commands.describe(
        prompt="Escreva QUASE tudo quiser, e a Inteligencia Artificial irá criar a imagem para você!",
        size="Defina em px, a largura e altura da imagem",
    )
    @app_commands.choices(
        size = [
            Choice(
                name='1024x1024',
                value=1024
            ),
            Choice(
                name='512x512',
                value=512
            ),
            Choice(
                name='256x256',
                value=256
            )
        ]
    )
    async def dall_e2(self, interaction:discord.Interaction, prompt:str, size:int=1024) -> None:
        try:
            await interaction.response.defer()
            
            load_dotenv()
            API_KEY = os.getenv("OPENAI_API_KEY")
            openai.api_key = API_KEY

            response = openai.Image.create(
                prompt=prompt,
                size=f"{size}x{size}", n=1
            )
            output = response['data'][0]['url']; pprint(output)


            embed = discord.Embed(
                colour=3426654,
                title='DALL・E 2',
                description=f'**Descrição:** {prompt}',
                url='https://openai.com/dall-e-2/'
            )
            embed.add_field(
                name='➭ Imagem Gerada',
                value=f'Tamanho da Imagem: {size}x{size}',
                inline=False
            )
            embed.set_image(url=output)
            await interaction.edit_original_response(embed=embed)

        except Exception as error:
            print(error)
    

async def setup(bot) -> None:
    await bot.add_cog(
        Generators(bot)
    )
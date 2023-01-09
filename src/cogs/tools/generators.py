import discord
from discord.ext import commands

from random import sample
import pyshorteners


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


async def setup(bot) -> None:
    await bot.add_cog(
        Generators(bot)
    )
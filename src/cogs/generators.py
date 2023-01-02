import discord
from discord.ext import commands

from random import sample
import pyshorteners


class Generators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='password_generator',
        help='Gera senhas aleatorias para você.',
        aliases=["password","gs","senha","gerar_senha"],
    )
    async def password_generator(self, ctx, size:int=16):
        try:
            caracters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()!"

            embed = discord.Embed(
                colour = 3447003,

                title = 'Aqui está a sua senha!',
                description = f'➭ Senha gerada: **{"".join(sample(caracters, size))}**'
            )
            await ctx.author.send(embed=embed)
            
            embed = discord.Embed(
                colour = 15418782,
                title = 'Sua senha foi lhe informada no privado!',
            )
            await ctx.send(embed=embed)
            
        except discord.errors.Forbidden:
            embed = discord.Embed(
                colour = 10038562,
                title = 'Infelizmente não consigo lhe enviar mensagens privadas!',
            )
            await ctx.send(embed=embed)


    @commands.command(
        name='shortlink',
        help='Encurta links para você!',
        aliases=["short","sl","encurtar"],
    )
    async def shortlink(self, ctx, link:str):
        short = pyshorteners.Shortener().tinyurl.short(link)
        
        embed = discord.Embed(
            colour = 3447003,

            title = 'Link Encurtado!',
            description = f'➭ **{short}**'
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Generators(bot))
import discord
from discord.ext import commands

from random import sample


class Password_generator(commands.Cog):
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


async def setup(bot):
    await bot.add_cog(Password_generator(bot))
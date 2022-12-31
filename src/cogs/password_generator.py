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

            await ctx.author.send(
                f'Senha gerada: **{"".join(sample(caracters, size))}**'
            )
            await ctx.send('**Sua senha foi lhe informada no privado!**')
            
        except discord.errors.Forbidden:
            await ctx.send('**Infelizmente não consigo lhe enviar mensagens privadas!**')


async def setup(bot):
    await bot.add_cog(Password_generator(bot))
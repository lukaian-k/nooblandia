import discord
from discord.ext import commands

import random
from numpy import number
from googlesearch import search

from src.system.json import *
from src.system.directories import *


BOT = dict(read_json(DIR_SECRET))

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()

        super().__init__(command_prefix=BOT["command_prefix"], case_insensitive=True, intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()

        if not self.synced:
            self.synced = True

bot = Bot()


@bot.command(name='calcular', help='Calculadora simples.')
async def calcular(ctx, n1:int, operacao, n2:int):
    if operacao == '+': resultado = [n1+n2]; resultado += ['soma']
    elif operacao == '-': resultado = [n1-n2]; resultado += ['subtração']
    elif operacao == '*': resultado = [n1*n2]; resultado += ['multiplicação']
    elif operacao == '/': resultado = [n1/n2]; resultado += ['divisão']
    await ctx.send(f'A {resultado[1]} dos número foi: {resultado[0]}')




@bot.command(name='google', help='Pesquise rápido no google pelo discord!', aliases=['g','pesquise'])
async def google(ctx, *args):
    await ctx.send(f'Aqui estão alguns dos resultados encontrados para "{" ".join(args)}":')
    for i in set(list(search(' '.join(args), num_results=5, lang="br"))):
        print(await ctx.send(str(i)))


@bot.command(
    name='gerar_senha',
    help='Gera senhas aleatorias para você.',
    aliases=["gs","senha"],
)
async def gerar_senha(ctx, tam:int=16):
    try:
        caracters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()!'
        await ctx.author.send(f'Senha gerada: **{"".join(random.sample(caracters, tam))}**')
        await ctx.send('Sua senha foi lhe informada no privado!')
        
    except discord.errors.Forbidden:
        await ctx.send('Infelizmente não consigo lhe enviar mensagens privadas!')


@bot.command(
    name='clear',
    help='Limpa até 100 mensagens do Chat.',
    aliases=["apaga","apagar","c"],
)
async def clear(ctx, amount=99):
    if ctx.author.guild_permissions.administrator:
        message = f'Mensagens apagadas com sucesso!\n\n**Total de mensagens apagadas: {amount}**'
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(message, delete_after=20)
    else:
        no_permission = 'Você não tem permissão para usar esse comando!'
        embed = discord.Embed(title=f'{no_permission}')
        await ctx.send(embed=embed)


bot.run(BOT["TOKEN"])
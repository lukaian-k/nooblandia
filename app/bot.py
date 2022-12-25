import discord
from discord.ext import commands
from googlesearch import search
import random
from numpy import number

from src.system.json import *
from src.system.directories import *


BOT = dict(read_json(DIR_SECRET))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix = BOT["command_prefix"], case_insensitive = True, intents=intents)


@bot.command(name='calcular', help='Calculadora simples.')
async def calcular(ctx, n1:int, operacao, n2:int):
    if operacao == '+': resultado = [n1+n2]; resultado += ['soma']
    elif operacao == '-': resultado = [n1-n2]; resultado += ['subtração']
    elif operacao == '*': resultado = [n1*n2]; resultado += ['multiplicação']
    elif operacao == '/': resultado = [n1/n2]; resultado += ['divisão']
    await ctx.send(f'A {resultado[1]} dos número foi: {resultado[0]}')


@bot.command(name='imc', help='Calculadora de imc.')
async def imc(ctx, peso:float, altura:float):
    resultado = peso/(altura*altura)
    if (resultado >= 18.5 and resultado <= 24.9): await ctx.send('Seu estado atual é: Peso Normal')
    elif (resultado >= 25 and resultado <= 29.9): await ctx.send('Seu estado atual é: Sobrepeso')
    elif (resultado >= 30 and resultado <= 34.9): await ctx.send('Seu estado atual é: Obesidade I')
    elif (resultado >= 35 and resultado <= 39.9): await ctx.send('Seu estado atual é: Obesidade II')
    elif (resultado >= 40 and resultado <= 49.9): await ctx.send('Seu estado atual é: Obesidade III')
    elif (resultado >= 50): await ctx.send('Seu estado atual é: Obesidade IV')
    elif (resultado < 18.5): await ctx.send('Seu estado atual é: Abaixo do peso')
    await ctx.send(f'Esse foi o resultado do seu IMC: {resultado}\nSe você estiver abaixo ou acima do peso normal, procure um médico!')


@bot.command(name='google', help='Pesquise rápido no google pelo discord!', aliases=['g','pesquise'])
async def google(ctx, *args):
    await ctx.send(f'Aqui estão alguns dos resultados encontrados para "{" ".join(args)}":')
    for i in set(list(search(' '.join(args), num_results=5, lang="br"))):
        print(await ctx.send(str(i)))


@bot.command(name='gerar_senha', help='Gera senhas aleatorias para você.')
async def gerar_senha(ctx, tam:int):
    caracters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()!'
    await ctx.send(f'Senha gerada: **{"".join(random.sample(caracters, tam))}**')


bot.run(BOT["TOKEN"])
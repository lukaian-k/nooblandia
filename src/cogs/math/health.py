import discord
from discord.ext import commands
from discord import app_commands


class Health(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(
        name='imc',
        description='Calculadora de imc.'
    )
    @app_commands.describe(
        peso="Insira o seu Peso.",
        altura="Insira a sua Altura.",
    )
    async def imc(self, interaction:discord.Interaction, peso:float, altura:float) -> None:
        result = round(
            peso/(altura*altura), 2
        )
        message = f"\n\n**Resultado do seu IMC: {result}**\nSe você estiver abaixo ou acima do peso normal, procure um médico!"
        
        conditions = {
            "Peso Normal": 18.5 <= result <= 24.9,
            "Sobrepeso": 25 <= result <= 29.9,
            "Abaixo do peso": result < 18.5,

            "Obesidade I": 30 <= result <= 34.9,
            "Obesidade II": 35 <= result <= 39.9,
            "Obesidade III": 40 <= result <= 49.9,
            "Obesidade IV": result >= 50,
        }

        colors = {
            "Peso Normal": 2067276,
            "Sobrepeso": 16705372,
            "Abaixo do peso": 15548997,

            "Obesidade I": 16705372,
            "Obesidade II": 15548997,
            "Obesidade III": 10038562,
            "Obesidade IV": 10038562,
        }

        reply = interaction.response
        
        for key in conditions:
            if conditions[key]:
                embed = discord.Embed(
                    colour = colors[key],
                
                    title = 'Seu estado atual é:',
                    description = f'➭ **{key}**{message}'
                )
                await reply.send_message(
                    ephemeral=True,
                    embed=embed
                )
                break
    

async def setup(bot) -> None:
    await bot.add_cog(
        Health(bot)
    )
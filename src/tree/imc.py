import discord
from discord import app_commands


async def fn_imc(interaction:discord.Interaction, peso:float, altura:float):
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
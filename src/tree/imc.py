import discord
from discord import app_commands


async def fn_imc(interaction:discord.Interaction, peso:float, altura:float):
    result = round(
        peso/(altura*altura), 2
    )
    message = f"\n\n**Esse foi o resultado do seu IMC: {result}**\nSe você estiver abaixo ou acima do peso normal, procure um médico!"
    
    conditions = {
        "Peso Normal": 18.5 <= result <= 24.9,
        "Sobrepeso": 25 <= result <= 29.9,
        "Obesidade I": 30 <= result <= 34.9,
        "Obesidade II": 35 <= result <= 39.9,
        "Obesidade III": 40 <= result <= 49.9,
        "Obesidade IV": result >= 50,
        "Abaixo do peso": result < 18.5,
    }

    reply = interaction.response
    
    for key in conditions:
        if (conditions[key] == True):
            await reply.send_message(
                f"Seu estado atual é: **{key}** {message}"
            )
            break
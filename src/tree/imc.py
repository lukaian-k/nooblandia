import discord
from discord import app_commands


async def fn_imc(interaction:discord.Interaction, peso:float, altura:float):
    result = peso/(altura*altura)
    message = f"\n\nEsse foi o resultado do seu IMC: {result}\nSe você estiver abaixo ou acima do peso normal, procure um médico!"
    
    reply = interaction.response
    
    if (result >= 18.5 and result <= 24.9): await reply.send_message(
        f"Seu estado atual é: Peso Normal {message}"
    )
    elif (result >= 25 and result <= 29.9): await reply.send_message(
        f"Seu estado atual é: Sobrepeso {message}"
    )
    elif (result >= 30 and result <= 34.9): await reply.send_message(
        f"Seu estado atual é: Obesidade I {message}"
    )
    elif (result >= 35 and result <= 39.9): await reply.send_message(
        f"Seu estado atual é: Obesidade II {message}"
    )
    elif (result >= 40 and result <= 49.9): await reply.send_message(
        f"Seu estado atual é: Obesidade III {message}"
    )
    elif (result >= 50): await reply.send_message(
        f"Seu estado atual é: Obesidade IV {message}"
    )
    elif (result < 18.5): await reply.send_message(
        f"Seu estado atual é: Abaixo do peso {message}"
    )
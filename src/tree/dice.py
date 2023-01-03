import discord
from discord import app_commands

from random import choice


async def dice(interaction:discord.Interaction, num_dice:int, sides:int):
    dice = [
        str(
            choice(
                range(
                    1,
                    sides+1
                )
            )
        )
        
        for _ in range(num_dice)
    ]

    dice = "(🎲 " + ")・(🎲 ".join(dice)

    embed = discord.Embed(
        colour = 2895667,
    
        title = 'Esses foram os resultados dos lançamentos:',
        description = f'**➭ {dice})**'
    )

    reply = interaction.response

    await reply.send_message(embed=embed)
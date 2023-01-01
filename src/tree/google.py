import discord
from discord import app_commands

from googlesearch import search


async def fn_google(interaction:discord.Interaction, search_for:str):
    print(f'\nBusca Por: {search_for}\n')

    found = list(
        set(
            search(
                search_for,
                num_results=5,
                lang="br"
            )
        )
    )

    icon = "➭ "
    found = icon + f'\n\n{icon}'.join(found)

    print(found)

    embed = discord.Embed(
        colour = 1146986,
    
        title = f'Aqui estão alguns dos resultados encontrados para ({search_for}):',
        description = found
    )

    reply = interaction.response

    await reply.send_message(
        ephemeral=True,
        embed=embed
    )
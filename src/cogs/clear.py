import discord
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='clear',
        help='Limpa até 100 mensagens do Chat.',
        aliases=["apaga","apagar","c"],
    )
    async def clear(self, ctx, amount=99):
        if ctx.author.guild_permissions.administrator:
            message = f'Total de mensagens apagadas: **{amount}**'

            embed = discord.Embed(
                colour = 15844367,
            
                title = 'Mensagens apagadas com sucesso!',
                description = message
            )
            await ctx.channel.purge(limit=amount+1)
            await ctx.send(
                embed=embed,
                delete_after=20
            )
        else:
            no_permission = 'Você não tem permissão para usar esse comando!'
            embed = discord.Embed(
                colour = 10038562,
                title=f'{no_permission}'
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Clear(bot))
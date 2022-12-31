import discord
from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        ame='clear',
        help='Limpa até 100 mensagens do Chat.',
        aliases=["apaga","apagar","c"],
    )
    async def clear(self, ctx, amount=99):
        bot = self.bot

        if ctx.author.guild_permissions.administrator:
            message = f'Mensagens apagadas com sucesso!\n\n**Total de mensagens apagadas: {amount}**'
            await ctx.channel.purge(limit=amount+1)
            await ctx.send(message, delete_after=20)
        else:
            no_permission = 'Você não tem permissão para usar esse comando!'
            embed = discord.Embed(title=f'{no_permission}')
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Clear(bot))
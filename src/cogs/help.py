import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='help',
        help='Comando de ajuda',
        aliases=['h', 'ajuda'],
    )
    async def help(self, ctx):
        bot = self.bot

        helptxt = ''
        for command in bot.commands:
            helptxt += f'**{command}:**\n{command.help}\n\n'

        embedhelp = discord.Embed(
            colour = 8592838, #purple
            title = f'{bot.user.name} Esses são meus comandos!',
            description = helptxt+'\n*Preparado?*'
        )
        embedhelp.set_thumbnail(url=bot.user.avatar.url)
        
        await ctx.send(embed=embedhelp)


async def setup(bot):
    await bot.add_cog(Help(bot))
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
        commands = bot.commands

        div = []
        for command in commands:
            div += [command.cog_name]
        div = list(set(div))

        tab = '・'
        helptxt = ''
        for name in div:
            helptxt += f'➭ *{name.upper()}*\n'

            for command in commands:
                if name == command.cog_name:
                    _name = f'{tab} **Nome do Comando:** | *{command}* |\n'
                    _help = f'{tab} **Sobre:** {command.help}\n'
                    _aliases = f'{tab} **Variações:** {" **-** ".join(command.aliases)}\n\n'

                    helptxt += f'{_name}{_help}{_aliases}'
                    
        embedhelp = discord.Embed(
            colour = 8592838, #purple
            title = f'{bot.user.name} Esses são meus comandos!',
            description = helptxt+'\n*Preparado?*'
        )
        embedhelp.set_thumbnail(url=bot.user.avatar.url)
        
        await ctx.send(embed=embedhelp)


async def setup(bot):
    await bot.add_cog(Help(bot))
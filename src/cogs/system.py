import discord
from discord.ext import commands


class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CheckFailure):
            no_permission = 'Você não tem permissão para usar esse comando!'

            embed = discord.Embed(
                colour = 10038562,
                title=f'{no_permission}'
            )
            await ctx.send(
                embed=embed,
                delete_after=20
            )
    

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
                    
        embed = discord.Embed(
            colour = 15277667,

            title = f'{bot.user.name} Esses são meus comandos!',
            description = helptxt+'\n*Preparado?*'
        )
        embed.set_thumbnail(url=bot.user.avatar.url)
        
        await ctx.send(embed=embed)
    

    @commands.command(
        name='send',
        help='Envie mensagens com o bot (uso restrito a admins).',
        aliases=["enviar","s"],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def send(self, ctx, channel:str, *message):
        bot = self.bot
        message = " ".join(message)

        print(f"message: {message}\nchannel: {channel}")

        MY_MESSAGE = 1
        await ctx.channel.purge(
            limit=MY_MESSAGE
        )
        
        channel = bot.get_channel(
            int(channel)
        )
        await channel.send(message)


    @commands.command(
        name='create_channel',
        help='Cria um novo canal no servidor (uso restrito a admins).',
        aliases=["cc","channel"],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def create_channel(self, ctx, *channel_name):
        channel_name = "-".join(channel_name)
        guild = ctx.guild

        existing_channel = discord.utils.get(
            guild.channels,
            name=channel_name
        )

        embed = discord.Embed()

        if not existing_channel:
            print(f'Creating a new channel: {channel_name}')

            embed.colour = 5763719
            embed.title = 'Novo canal criado!'
            embed.description = f'➭ Nome: **{channel_name}**'

            await guild.create_text_channel(channel_name)
        else:
            embed.colour = 15548997
            embed.title = 'Algo deu errado!'
            embed.description = f'➭ O Canal **{channel_name}** já existe.'
        
        await ctx.reply(embed=embed)


    @commands.command(
        name='clear',
        help='Limpa até 100 mensagens do Chat.',
        aliases=["apaga","apagar","c"],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def clear(self, ctx, amount=99):
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


async def setup(bot):
    await bot.add_cog(System(bot))
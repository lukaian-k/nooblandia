import discord
from discord.ext import commands


class Management(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
        with_app_command=True,

        name='help',
        description='Comando de ajuda!',

        help='Comando de ajuda!',
        aliases=['h','ajuda'],
    )
    async def help(self, ctx:commands.Context) -> None:
        bot = self.bot
        commands = bot.commands

        div = []
        for command in commands:
            div += [command.cog_name]
        div = list(set(div))

        embed = discord.Embed(
            colour = 15277667,

            title = f'Oi eu sou a **{bot.user.name}!**',
            description = '➥ Esses são meus **comandos:**'
        )
        embed.set_thumbnail(url=bot.user.avatar.url)

        tab = '・'
        for name in div:

            for command in commands:

                if name == command.cog_name:

                    _name = f'*{name.upper()}*{tab}Nome do Comando: (*{command}*)'
                    _help = f'{tab} **Sobre:** {command.help}\n'
                    _aliases = f'{tab} **Variações:** {" **-** ".join(command.aliases)}'

                    embed.add_field(
                        name=f'➭ {_name}',
                        value=f'{_help}{_aliases}',
                        inline=False
                    )
                    
        await ctx.send(embed=embed)
    

    @commands.command(
        name='send',
        help='Envie mensagens com o bot (uso restrito a admins).',
        aliases=["enviar","s"],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def send(self, ctx, channel:str, *message) -> None:
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
    async def create_channel(self, ctx, *channel_name) -> None:
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


    @commands.hybrid_command(
        with_app_command=True,
        
        name='clear',
        description='Limpa até 100 mensagens do Chat.',
        
        help='Limpa até 100 mensagens do Chat.',
        aliases=['apagar','c'],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def clear(self, ctx:commands.Context, amount:int=100) -> None:
        embed = discord.Embed()

        if amount < 2:
            embed.colour = 15548997
            embed.title = 'Só é possível apagar 2 ou mais mensagens!'

            await ctx.reply(
                embed=embed,
                ephemeral=True,
                delete_after=20
            ); return

        await ctx.reply(
            'https://tenor.com/view/deleted-cat-unsent-unsend-message-gif-26266359',
            ephemeral=True,
            delete_after=10
        )
        message = f'Total de mensagens apagadas: **{amount}**'

        embed.colour = 15844367
        embed.title = 'Mensagens apagadas com sucesso!'
        embed.description = message

        await ctx.channel.purge(limit=amount)
        await ctx.send(
            embed=embed,
            delete_after=20
        )


async def setup(bot) -> None:
    await bot.add_cog(
        Management(bot)
    )
import discord
from discord.ext import commands
from discord import app_commands

import io
from random import randint, choice
from PIL import Image, ImageFont, ImageDraw, ImageOps


class Entertainments(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        self.what_is = None
        self.ctx = None

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user) -> None:
        if self.what_is != 'game':
            return
        bot = self.bot
        
        message = reaction.message
        emoji = str(reaction.emoji)

        is_user = user != bot.user

        if is_user and emoji == '🇹':
            await message.remove_reaction('🇹', user)
            
            await message.remove_reaction('🇹', bot.user)
            await message.remove_reaction('♟️', bot.user)
            await message.remove_reaction('❌', bot.user)
            
        elif is_user and emoji == '❌':
            embed = discord.Embed(
                colour=15548997,
                title='Cancelado!'
            )
            await self.ctx.send(
                embed=embed,
                delete_after=10
            )
            await message.delete()
    

    @commands.command(
        name='game',
        help='Hub de seleção de jogo.',
        aliases=["j","jogar"],
    )
    async def game(self, ctx) -> None:
        self.what_is = 'game'
        self.ctx = ctx
        
        games = {
            "Tetris": '🇹',
            "Xadrez": '♟️',
        }

        embed = discord.Embed(
            colour=9807270,
            title='Aguarde...'
        )
        message = await ctx.send(embed=embed)


        embed.colour = 11027200
        embed.title = '➭ Jogos'
        embed.description = 'Selecione o que deseja **jogar**!'

        for name in games:
            await message.add_reaction(games[name])

            embed.add_field(
                name=f'Pressione ➥ {games[name]}',
                value=f'Para jogar・**{name}**',
                inline=False
            )
        await message.add_reaction('❌')
        await message.edit(embed=embed)


    @app_commands.command(
        name='ship',
        description='Qual será as chances de termos um casalzão 20 por aqui?!'
    )
    @app_commands.describe(
        primeira="Marque a primeira pessoa...",
        segunda="Marque a segunda pessoa...",
    )
    async def ship(self, interaction:discord.Interaction, primeira:discord.User, segunda:discord.User) -> None:
        message = "🏹 **Vamos ver se teremos um casalzão 20 por aqui!** 💕"

        if primeira.name == segunda.name:
            nameship = "Amor próprio é tudo!"
            percent = 100
            
        else:
            step_name1 = primeira.name[:len(primeira.name)//2]
            step_name2 = segunda.name[len(segunda.name)//2:]
            nameship = step_name1+step_name2

            percent = randint(0,100)

        mention = f"{primeira.mention} **+** {segunda.mention} **= {nameship}**"

        react = "😍\n\nOlha o casalzão chegando na área! 🤩🤩🤩" if percent >= 50 else "😢\n\nParece que não teremos um casal 20 😭😭😭"
        chances = f"💘 Tem **{percent}%** de chances de darem certo! **{react}**"


        icon1 = await primeira.avatar.read()
        avatar1 = Image.open(io.BytesIO(icon1))
        avatar1 = avatar1.resize((250,250))

        icon2 = await segunda.avatar.read()
        avatar2 = Image.open(io.BytesIO(icon2))
        avatar2 = avatar2.resize((250,250))

        background = Image.new("RGB",(500,260),(237, 196, 213))
        background.paste(avatar1,(0,0))
        background.paste(avatar2,(250,0))

        draw_rectangle = ImageDraw.Draw(background)
        init_draw = (0,250)
        end_draw = (500*(percent/100),260)
        draw_rectangle.rectangle(
            (init_draw,end_draw),
            fill="#fff",
        )

        font = ImageFont.truetype("assets/fonts/ship.ttf",50)
        draw_rectangle.text(
            (210,90),
            f"{percent}%",
            font=font,
            stroke_fill="#000",
            stroke_width=3
        )

        draw_rectangle.text(
            (
                ( (250-20)/2 ),
                ( 180 )
            ),
            f"{primeira.name[0].upper()}",
            font=font,
            stroke_fill="#000",
            stroke_width=5
        )
        draw_rectangle.text(
            (
                ( ((250-5)/2)*3 ),
                ( 180 )
            ),
            f"{segunda.name[0].upper()}",
            font=font,
            stroke_fill="#000",
            stroke_width=5
        )

        
        buffer = io.BytesIO()
        background.save(buffer,format="PNG")
        buffer.seek(0)

        await interaction.response.send_message(
            f"{message}\n\n{mention} {chances}",
            file=discord.File(fp=buffer,filename=f"{nameship}.png")
        )


    @commands.hybrid_command(
        with_app_command=True,

        name='rolar_dados',
        description='Simula uma jogada de dado.',

        help='Simula uma jogada de dado.',
        aliases=['d','dice'],
    )
    @app_commands.describe(
        quantos_dados="Quantidade de dados a serem rolados.",
        lados="Quantos lados o dado terá.",
    )
    async def rolar_dados(self, ctx:commands.Context, quantos_dados:int, lados:int) -> None:
        dice = [
            str(
                choice(
                    range(
                        1,
                        lados+1
                    )
                )
            )
            
            for _ in range(quantos_dados)
        ]

        dice = "(🎲 " + ")・(🎲 ".join(dice)

        embed = discord.Embed(
            colour = 2895667,
        
            title = 'Esses foram os resultados dos lançamentos:',
            description = f'**➭ {dice})**'
        )
        await ctx.reply(embed=embed)

    
async def setup(bot) -> None:
    await bot.add_cog(
        Entertainments(bot)
    )
import discord
from discord import app_commands

from random import randint
import io
from PIL import Image, ImageFont, ImageDraw, ImageOps


async def ship(interaction:discord.Interaction, user1:discord.User, user2:discord.User):
    message = "🏹 **Vamos ver se teremos um casalzão 20 por aqui!** 💕"

    if user1.name == user2.name:
        nameship = "Amor próprio é tudo!"
        percent = 100
        
    else:
        step_name1 = user1.name[:len(user1.name)//2]
        step_name2 = user2.name[len(user2.name)//2:]
        nameship = step_name1+step_name2

        percent = randint(0,100)

    mention = f"{user1.mention} **+** {user2.mention} **= {nameship}**"

    react = "😍\n\nOlha o casalzão chegando na área! 🤩🤩🤩" if percent >= 50 else "😢\n\nParece que não teremos um casal 20 😭😭😭"
    chances = f"💘 Tem **{percent}%** de chances de darem certo! **{react}**"


    icon1 = await user1.avatar.read()
    avatar1 = Image.open(io.BytesIO(icon1))
    avatar1 = avatar1.resize((250,250))

    icon2 = await user2.avatar.read()
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
        f"{user1.name[0].upper()}",
        font=font,
        stroke_fill="#000",
        stroke_width=5
    )
    draw_rectangle.text(
        (
            ( ((250-5)/2)*3 ),
            ( 180 )
        ),
        f"{user2.name[0].upper()}",
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
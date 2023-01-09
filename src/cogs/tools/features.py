import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice

import pyaudio
import wave

from youtube_dl import YoutubeDL

from src.system.system import clear_dir


class Features(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        self.what_is = None
        self.ctx = None
        self.duration = None

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user) -> None:
        if self.what_is != 'record':
            return
        bot = self.bot
        
        message = reaction.message
        emoji = str(reaction.emoji)

        is_user = user != bot.user

        if is_user and emoji == '▶':
            await message.remove_reaction('▶', user)
            
            await message.remove_reaction('▶', bot.user)
            await message.remove_reaction('❌', bot.user)
            
            await self.recording(message)

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
    

    @commands.hybrid_command(
        with_app_command=True,

        name='record',
        description='Grave audios para enviar no discord!',

        help='Grave audios para enviar no discord!',
        aliases=['r','gravar'],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def record(self, ctx:commands.Context, duration:int=10) -> None:
        embed = discord.Embed()
        
        if not ctx.author.voice:
            embed.colour = 15548997
            embed.title = 'Você precisa estar em um canal de voz para usar esse comando.'
            await ctx.reply(
                embed=embed,
                delete_after=10
            )
            return

        if duration > 30:
            embed.colour = 15548997
            embed.title = 'Limite de Tempo excedido!'
            embed.description = 'Máximo: **30 segundos**'
            await ctx.reply(
                embed=embed,
                delete_after=10
            )
            return

        self.what_is = 'record'
        self.ctx = ctx
        self.duration = duration


        embed.colour=5793266
        embed.title='Gravador de Audios'
        embed.description=f'Grave e envie audios no **Discord**'

        embed.add_field(
            name='Como usar:',
            value=f'Pressione o botão ▶ para gravar o audio.\n\nDuração do audio: **{duration}s**',
            inline=False
        )
        message = await ctx.send(embed=embed)

        await message.add_reaction('▶')
        await message.add_reaction('❌')

    async def recording(self, message) -> None:
        ctx = self.ctx
        duration = self.duration

        author = ctx.message.author
        channel = author.voice.channel
        voice_client = await channel.connect()

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        SECONDS = duration+1
        DIRECTORY = "assets/recordings/audio.wav"


        audio = pyaudio.PyAudio()

        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        audio_data = []

        embed = discord.Embed(
            colour = 16705372,

            title = '➭ Gravação iniciada!',
            description = f'Duração da gravação: **{duration}s**'
        )
        await message.edit(embed=embed)

        for i in range(0, int(RATE/CHUNK*SECONDS)):
            data = stream.read(CHUNK)
            audio_data.append(data)
        audio_data = b''.join(audio_data)

        embed.colour = 5763719
        embed.title = 'Gravação concluida!'
        embed.description = None
        await message.edit(
            embed=embed,
            delete_after=10
        )


        stream.stop_stream()
        stream.close()
        audio.terminate()
        await voice_client.disconnect()

        file = wave.open(DIRECTORY, 'wb')
        file.setnchannels(CHANNELS)
        file.setsampwidth(audio.get_sample_size(FORMAT))
        file.setframerate(RATE)
        file.writeframes(audio_data)
        file.close()


        embed.colour = 5763719
        embed.title = 'Mensagem de Voz'
        embed.description = f'➭ Send by: **{author.name}**・Duração: **{duration}s**'

        with open(DIRECTORY, 'rb') as file:
            await ctx.send(
                file=discord.File(file),
                embed=embed
            )
    

    @app_commands.command(
        name='download',
        description='Faz download de videos do YouTube apartir de links.'
    )
    @app_commands.describe(
        link="Link do vídeo do YouTube que deseja baixar!",
        ext="Formato do Arquivo.",
    )
    @app_commands.choices(
        ext = [
            Choice(
                name='Vídeo ➭ mp4',
                value='mp4'
            ),
            Choice(
                name='Vídeo ➭ mov',
                value='mov'
            ),
            Choice(
                name='Vídeo ➭ mkv',
                value='mkv'
            ),
            Choice(
                name='Áudio ➭ mp3',
                value='mp3'
            ),
            Choice(
                name='Áudio ➭ wav',
                value='wav'
            ),
            Choice(
                name='Áudio ➭ ogg',
                value='ogg'
            )
        ]
    )
    async def download(self, interaction:discord.Interaction, link:str, ext:str) -> None:
        await interaction.response.defer()

        ydl_opts = {
            "format": f'bestvideo[ext={ext}]+bestaudio[ext=m4a]/best[ext={ext}]/best',
            "outtmpl": f'assets/downloads/temp.{ext}',
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                link = [link.strip()]
                ydl.download(link)

                embed = discord.Embed(
                    colour = 5763719,
                    title = 'Download Concluido!',
                    description = '➭ Aqui está o **seu pedido**!'
                )

                with open(ydl_opts["outtmpl"], 'rb') as file:
                    user = interaction.user
                    file = discord.File(file, filename=f'pedido_de_{user}.{ext}')

                    await interaction.edit_original_response(
                        attachments=[file],
                        embed=embed
                    )
                    
            except Exception as error:
                print(error)
                
                embed = discord.Embed(
                    colour = 15548997,
                    title = 'Algo deu errado!',
                    description = 'Não foi possível **baixar ou enviar** o vídeo'
                )
                await interaction.edit_original_response(embed=embed)

        clear_dir('assets/downloads')


async def setup(bot) -> None:
    await bot.add_cog(
        Features(bot)
    )
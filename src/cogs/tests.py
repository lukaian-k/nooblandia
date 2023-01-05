import discord
from discord.ext import commands

import pyaudio
import wave


class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='record',
        help='Grave audios para enviar no discord!',
        aliases=['r', 'gravar'],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def record(self, ctx, duration:int=10):
        embed = discord.Embed()

        if not ctx.author.voice or ctx.author.voice.channel != ctx.me.voice.channel:
            embed.colour = 15548997
            embed.title = "Você precisa estar em um canal de voz para usar esse comando."
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

        embed.colour = 16705372
        embed.title = '➭ Gravação iniciada!'
        embed.description = f'Duração da gravação: **{duration}s**'
        message = await ctx.reply(embed=embed)

        for i in range(0, int(RATE/CHUNK*SECONDS)):
            data = stream.read(CHUNK)
            audio_data.append(data)

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
        file.writeframes(b''.join(audio_data))
        file.close()


        embed.colour = 5763719
        embed.title = 'Mensagem de Voz:!'
        embed.description = f'➭ Send by: **{author.name}**・Duração: **{duration}s**'

        with open(DIRECTORY, 'rb') as file:
            await ctx.send(
                file=discord.File(file),
                embed=embed
            )


async def setup(bot):
    await bot.add_cog(Tests(bot))
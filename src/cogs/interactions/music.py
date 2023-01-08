import discord
from discord.ext import commands

import re
from youtube_dl import YoutubeDL

import asyncio
from pprint import pprint


URL_REG = re.compile(r'https?://(?:www\.)?.+')
YOUTUBE_VIDEO_REG = re.compile(r"(https?://)?(www\.)?youtube\.(com|nl)/watch\?v=([-\w]+)")

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.event = asyncio.Event()

        self.music_queue = []
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            #'default_search': 'auto',
            'extract_flat': True,
        }
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn',
        }

        self.you = ""


    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                if (yt_url:=YOUTUBE_VIDEO_REG.match(item)):
                    item = yt_url.group()
                elif not URL_REG.match(item):
                    item = f"ytsearch:{item}"

                info = ydl.extract_info(
                    item,
                    download=False
                )
            except Exception: 
                return False

        try:
            entries = info["entries"]
        except KeyError:
            entries = [info]

        if info["extractor_key"] == "YoutubeSearch":
            entries = entries[:1]

        tracks = []

        for t in entries:
            tracks.append(
                {
                    'source': f'https://www.youtube.com/watch?v={t["id"]}',
                    'title': t['title'],
                }
            )

        return tracks


    async def play_music(self):
        self.event.clear()

        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            with YoutubeDL(self.YDL_OPTIONS) as ydl:
                try:
                    info = ydl.extract_info(
                        m_url,
                        download=False
                    )
                    m_url = info['formats'][0]['url']
                except Exception:
                    return False

            if self.you == "" or not self.you.is_connected() or self.you == None:
                self.you = await self.music_queue[0][1].connect()
            else:
                await self.you.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.you.play(
                discord.FFmpegPCMAudio(
                    m_url,
                    **self.FFMPEG_OPTIONS
                ),
                after=lambda l: self.bot.loop.call_soon_threadsafe(self.event.set)
            )
            await self.event.wait()
            await self.play_music()
        else:
            self.is_playing = False
            self.music_queue.clear()
            await self.you.disconnect()


    @commands.command(
        name="play",
        help="Toca uma música do YouTube",
        aliases=['p','tocar'],
    )
    async def play(self, ctx:commands.Context, *, query:str="PÉRICLES - ATÉ QUE DUROU (AO VIVO) - VÍDEO OFICIAL"):
        try:
            voice_channel = ctx.author.voice.channel
        except:
            embed = discord.Embed(
                colour=15548997,
                description='Para tocar uma música, primeiro se conecte a um canal de voz.'
            )
            await ctx.send(embed=embed)
            return
        else:
            songs = self.search_yt(query)
            
            if type(songs) == type(True):
                embed = discord.Embed(
                    colour=15548997,
                    description='Algo deu errado! Tente mudar ou configurar a playlist/vídeo ou escrever o nome dele novamente!'
                )
                await ctx.send(embed=embed)
            else:
                if (size:=len(songs)) > 1:
                    txt = f"Você adicionou **{size} músicas** na fila!"
                else:
                    txt = f"Você adicionou a música **{songs[0]['title']}** à fila!"

                embed = discord.Embed(
                    colour= 5763719,
                    description = f"{txt}\n\n**Divirta-se!**"
                )
                await ctx.send(embed=embed)

                for song in songs:
                    self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music()


    @commands.command(
        name="queue",
        help="Mostra as atuais músicas da fila.",
        aliases=['q','fila'],
    )
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f'**{i+1} - **' + self.music_queue[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            embed = discord.Embed(
                colour=11342935,
                description=f"{retval}"
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=10038562,
                description='Não existe músicas na fila no momento.'
            )
            await ctx.send(embed=embed)


    @commands.command(
        name="skip",
        help="Pula a atual música que está tocando.",
        aliases=['pular','passar','sk'],
    )
    @commands.has_permissions(
        manage_channels=True
    )
    async def skip(self, ctx):
        if self.you != "" and self.you:
            self.you.stop()

            embed = discord.Embed(
                colour=2899536,
                description=f"Você pulou a música."
            )
            await ctx.send(embed=embed)

    @skip.error
    async def skip_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour=15548997,
                description=f"Você precisa da permissão **Gerenciar canais** para pular músicas."
            )
            await ctx.send(embed=embed)     
        else:
            raise error


    @commands.command(
        name="stop",
        help="Para o player de tocar músicas",
        aliases=["parar", "sair", "leave", "l"],
    )
    async def stop(self, ctx: commands.Context):
        embed = discord.Embed(colour=15548997)

        if not ctx.me.voice:
            embed.description = "Não estou conectado em um canal de voz."
            await ctx.reply(embed=embed)
            return

        if not ctx.author.voice or ctx.author.voice.channel != ctx.me.voice.channel:
            embed.description = "Você precisa estar no meu canal de voz atual para usar esse comando."
            await ctx.reply(embed=embed)
            return

        if any(m for m in ctx.me.voice.channel.members if not m.bot and m.guild_permissions.manage_channels) and not ctx.author.guild_permissions.manage_channels:
            embed.description = "No momento você não tem permissão para usar esse comando."
            await ctx.reply(embed=embed)
            return

        self.is_playing = False
        self.music_queue.clear()
        await self.you.disconnect(force=True)

        embed.colour = 10038562
        embed.description = "Você parou o player"
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))
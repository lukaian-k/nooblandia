import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        #All the music related stuff
        self.is_playing = False

        #2d array containing [song, channel]
        self.music_list = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""

    #Searching the item on youtube
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_list) > 0:
            self.is_playing = True

            #Get the first url
            m_url = self.music_list[0][0]['source']

            #Remove the first element as you are currently playing it
            self.music_list.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False

    #Download
    def download_music(self, d_item):
        with YoutubeDL(self.YDL_OPTIONS) as d_ydl:
            try:
                inf = d_ydl.extract_info("ytsearch:%s" % d_item, download=True)['entries'][0]
            except Exception: 
                return False

        return {'source': inf['formats'][0]['url'], 'title': inf['title']}

    #Infinite loop checking 
    async def play_music(self):
        if len(self.music_list) > 0:
            self.is_playing = True

            m_url = self.music_list[0][0]['source']
            
            #Try to connect to voice channel if you are not already connected
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_list[0][1].connect()
            else:
                await self.vc.move_to(self.music_list[0][1])
            
            print(self.music_list)

            #Remove the first element as you are currently playing it
            self.music_list.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after = lambda e: self.play_next())
        else:
            self.is_playing = False
            await self.vc.disconnect()

    #Commands - Play
    @commands.command(name = "play", help = "Toca uma música do YouTube", aliases = ['p','tocar'])
    async def play(self, ctx, *args):
        query = " ".join(args)
        
        try:
            voice_channel = ctx.author.voice.channel
        except:
        #If voice_channel is None:
            #You need to be connected so that the bot knows where to go
            embedvc = discord.Embed(
                colour = 12984106, #Red
                description = 'Para tocar uma música, primeiro se conecte a um canal de voz.'
            )
            await ctx.send(embed = embedvc)
            return
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                embedvc = discord.Embed(
                    colour= 12984106, #Red
                    description = 'Algo deu errado! Tente mudar ou configurar a playlist/vídeo ou escrever o nome dele novamente!'
                )
                await ctx.send(embed = embedvc)
            else:
                embedvc = discord.Embed(
                    colour = 1553713, #Green
                    description = f"Você adicionou a música **{song['title']}** à fila! \n\n Divirta-se!"
                )
                await ctx.send(embed=embedvc)
                self.music_list.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()

    #Commands - List
    @commands.command(name = "list", help = "Mostra as atuais músicas da fila", aliases = ['f', 'fila'])
    async def list(self, ctx):
        retval = ""
        for i in range(0, len(self.music_list)):
            retval += f'**{i+1} - **' + self.music_list[i][0]['title'] + "\n"

        print(retval)
        if retval != "":
            embedvc = discord.Embed(
                colour = 8592838, #Purple
                description = f"{retval}"
            )
            await ctx.send(embed = embedvc)
        else:
            embedvc = discord.Embed(
                colour = 12984106, #Red
                description = 'Não existe músicas na fila no momento.'
            )
            await ctx.send(embed = embedvc)

    #Commands - Skip
    @commands.command(name ="skip", help = "Pula a atual música que está tocando", aliases = ['sk', 'pular'])
    @commands.has_permissions(manage_channels = True)
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            
            #Try to play next in the list if it exists
            await self.play_music()
            embedvc = discord.Embed(
                colour = 1553713, #Green
                description = f"Você pulou a música."
            )
            await ctx.send(embed = embedvc)

    @skip.error #Erros para kick
    async def skip_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            embedvc = discord.Embed(
                colour= 12984106, #Red
                description = f"Você precisa da permissão **Gerenciar canais** para pular músicas."
            )
            await ctx.send(embed=embedvc)     
        else:
            raise error

    #Commands - Stop
    @commands.command(name = "stop", help = "Desconecta o Bot da Call", aliases = ["parar", "sair", "leave", "l"])
    async def stop(self, ctx: commands.Context):
        embedvc = discord.Embed(colour= 12984106) #Red

        if not ctx.me.voice:
            embedvc.description = "Não estou conectado em um canal de voz."
            await ctx.reply(embed = embedvc)
            return

        if not ctx.author.voice or ctx.author.voice.channel != ctx.me.voice.channel:
            embedvc.description = "Você precisa estar no meu canal de voz atual para usar esse comando."
            await ctx.reply(embed=embedvc)
            return

        if any(m for m in ctx.me.voice.channel.members if not m.bot and m.guild_permissions.manage_channels) and not ctx.author.guild_permissions.manage_channels:
            embedvc.description = "No momento você não tem permissão para usar esse comando."
            await ctx.reply(embed = embedvc)
            return

        self.is_playing = False
        self.music_list.clear()
        await self.vc.disconnect(force = True)

        embedvc.colour = 12984106 #Red
        embedvc.description = "Você parou o player"
        await ctx.reply(embed = embedvc)

    #Commands - Download
    @commands.command(name = "download", help = "Baixa a música escolhida・**Ex.:** _download até que durou", aliases = ['b', 'baixar'])
    async def download(self, ctx, *args):
        query = " ".join(args)
        
        try:
            voice_channel = ctx.author.voice.channel
        except:
        #If voice_channel is None:
            #You need to be connected so that the bot knows where to go
            embedvc = discord.Embed(
                colour = 12984106, #Red
                description = 'Para tocar uma música, primeiro se conecte a um canal de voz.'
            )
            await ctx.send(embed=embedvc)
            return
        else:
            song = self.download_music(query)
            if type(song) == type(True):
                embedvc = discord.Embed(
                    colour= 12984106, #Red
                    description = 'Algo deu errado! Tente mudar ou configurar a playlist/vídeo ou escrever o nome dele novamente!'
                )
                await ctx.send(embed=embedvc)
            else:
                embedvc = discord.Embed(
                    colour= 1553713, #Green
                    description = f"Você adicionou a música **{song['title']}** à fila! \n\n Divirta-se!"
                )
                await ctx.send(embed=embedvc)
                self.music_list.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()


async def setup(bot):
    await bot.add_cog(Music(bot))
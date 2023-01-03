import discord
from discord.ext import commands

from youtube_dl import YoutubeDL

from src.system.system import clear_dir


class Features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='download',
        help='Faz download de videos do YouTube apartir de links.',
        aliases=["d","baixar"],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def download(self, ctx, link:str, ext:str):
        ydl_opts = {
            "format": f'bestvideo[ext={ext}]+bestaudio[ext=m4a]/best[ext={ext}]/best',
            "outtmpl": f'assets/downloads/temp.{ext}',
        }

        with YoutubeDL(ydl_opts) as ydl:
            try:
                embed = discord.Embed(
                    colour = 5793266,

                    title = '➭ Tudo Certo!',
                    description = '*Apenas aguarde o download ser concluido...*'
                )
                await ctx.reply(embed=embed)

                link = [link.strip()]
                ydl.download(link)

                embed.colour = 5763719
                embed.title = 'Download Concluido!'
                embed.description = '➭ *Aqui está o **seu pedido**!*'

                with open(ydl_opts["outtmpl"], 'rb') as file:
                    await ctx.reply(
                        file=discord.File(file),
                        embed=embed
                    )
            except:
                embed = discord.Embed(
                    colour = 15548997,
                    title = 'Algo deu errado!',
                    description = 'Não foi possível **baixar ou enviar** o vídeo'
                )
                await ctx.reply(embed=embed)

        clear_dir('assets/downloads')


async def setup(bot):
    await bot.add_cog(Features(bot))
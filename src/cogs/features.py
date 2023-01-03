import discord
from discord.ext import commands

from youtube_dl import YoutubeDL


class Features(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='download',
        help='Faz download de videos do youtube apartir de links.',
        aliases=["d","baixar"],
    )
    @commands.has_permissions(
        administrator=True,
    )
    async def download(self, ctx, link:str):
        with YoutubeDL() as ydl:
            try:
                embed = discord.Embed(
                    colour = 5793266,

                    title = '➭ Tudo Certo!',
                    description = '*Apenas aguarde o download ser concluido...*'
                )
                await ctx.reply(embed=embed)

                link = [link.strip()]
                ydl.download(link)

                embed.colour = 10070709
                embed.title = 'Download Concluido!'
                embed.description = None
                await ctx.reply(embed=embed)
            except:
                embed = discord.Embed(
                    colour = 15548997,
                    title = 'Não foi possível fazer o download do vídeo',
                )
                await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Features(bot))
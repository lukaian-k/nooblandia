import discord
from discord.ext import commands


class Send(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='send',
        help='Envie mensagens com o bot (uso restrito a admins).',
        aliases=["enviar","s"],
    )
    async def send(self, ctx, channel:str, *message):
        bot = self.bot
        message = " ".join(message)

        permission = ctx.author.guild_permissions.administrator

        if permission != True:
            ctx.send("**Vocé não tem permisão para usar esse comando!**", delete_after=20)
            return

        print(f"message: {message}\nchannel: {channel}")

        MY_MESSAGE = 1
        await ctx.channel.purge(
            limit=MY_MESSAGE
        )
        
        channel = bot.get_channel(
            int(channel)
        )
        await channel.send(message)


async def setup(bot):
    await bot.add_cog(Send(bot))
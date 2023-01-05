import discord
from discord.ext import commands


class Entertain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.what_is = None
        self.ctx = None

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
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
    async def game(self, ctx):
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

    
async def setup(bot):
    await bot.add_cog(Entertain(bot))
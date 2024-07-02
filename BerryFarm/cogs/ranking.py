import discord
from discord.ext import commands
import json

class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ranking")
    async def ranking(self, ctx):
        with open('banco.json', 'r') as f:
            banco = json.load(f)

        
        sorted_banco = sorted(banco.items(), key=lambda x: x[1], reverse=True)

        
        embed = discord.Embed(title="Ranking", description="membros mais ricos do servidor:", color=discord.Color.gold())

        for i, (user_id, saldo) in enumerate(sorted_banco[:10], start=1):  
            user = self.bot.get_user(int(user_id))
            if user:
                embed.add_field(name=f"{i}. {user.name}", value=f"💰 {saldo} moedas", inline=False)
            else:
                embed.add_field(name=f"{i}. Usuário desconhecido", value=f"💰 {saldo} moedas", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Ranking(bot))

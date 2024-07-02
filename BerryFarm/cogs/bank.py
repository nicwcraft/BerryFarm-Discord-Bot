import discord
from discord.ext import commands
import json
import os

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bank_file = 'banco.json'

    def load_bank_data(self):
        if os.path.isfile(self.bank_file):
            with open(self.bank_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_bank_data(self, bank_data):
        with open(self.bank_file, 'w') as f:
            json.dump(bank_data, f, indent=4)

    @commands.command()
    async def saldo(self, ctx):
        user_id = str(ctx.author.id)
        bank_data = self.load_bank_data()
        saldo = bank_data.get(user_id, 0)
        
        embed = discord.Embed(
            title="Saldo Bancário",
            description=f"Você atualmente possui <:emoji_9:1243058689104019466> **{saldo} Moedas!!**",
            color=discord.Color(int('008000', 16))
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Bank(bot))

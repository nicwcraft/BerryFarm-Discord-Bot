import discord
from discord.ext import commands
import json
import os

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.farm_file = 'fazenda.json'
        self.bank_file = 'banco.json'
        self.morango_preco = 5  

    def load_farm_data(self):
        if os.path.isfile(self.farm_file):
            with open(self.farm_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_farm_data(self, farm_data):
        with open(self.farm_file, 'w') as f:
            json.dump(farm_data, f, indent=4)

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
    async def vender(self, ctx, quantidade: int = None):
        user_id = str(ctx.author.id)
        farm_data = self.load_farm_data()
        
        if user_id not in farm_data or farm_data[user_id] == 0:
            await ctx.send("Você não tem morangos para vender.")
            return

        if quantidade is None:
            quantidade = farm_data[user_id]

        if quantidade > farm_data[user_id]:
            await ctx.send("Você não tem morangos suficientes para vender essa quantidade.")
            return

        farm_data[user_id] -= quantidade
        dinheiro_ganho = quantidade * self.morango_preco
        bank_data = self.load_bank_data()
        
        if user_id in bank_data:
            bank_data[user_id] += dinheiro_ganho
        else:
            bank_data[user_id] = dinheiro_ganho

        self.save_farm_data(farm_data)
        self.save_bank_data(bank_data)
        
        embed = discord.Embed(
            title="Morangos Vendidos",
            description=f"{ctx.author.mention} Vendeu habilmente a colheita de <:emoji_14:1253421914630656020> **{quantidade} Morangos**, recebendo em troca um generoso pagamento de <:emoji_9:1243058689104019466> **{dinheiro_ganho} Moedas.**",
            color=discord.Color(int('008000', 16))
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Shop(bot))

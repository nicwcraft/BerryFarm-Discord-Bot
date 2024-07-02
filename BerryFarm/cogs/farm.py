import discord
from discord.ext import commands
import json
import os
from datetime import datetime, timedelta

class Farm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.farm_file = 'fazenda.json'
        self.plant_file = 'plantados.json'
        self.max_plant_per_period = 10  # Máximo de morangos que podem ser plantados por período
        self.plant_cooldown = 10 * 60  # Cooldown de 30 minutos em segundos
        self.user_plant_data = {}  # Armazena os dados de plantio dos usuários

    def load_farm_data(self):
        if os.path.isfile(self.farm_file):
            with open(self.farm_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_farm_data(self, farm_data):
        with open(self.farm_file, 'w') as f:
            json.dump(farm_data, f, indent=4)

    def load_plant_data(self):
        if os.path.isfile(self.plant_file):
            with open(self.plant_file, 'r') as f:
                return json.load(f)
        else:
            return {}

    def save_plant_data(self, plant_data):
        with open(self.plant_file, 'w') as f:
            json.dump(plant_data, f, indent=4)

    @commands.command()
    async def plantar(self, ctx, quantidade: int = 1):
        user_id = str(ctx.author.id)
        current_time = datetime.now()
        
        if quantidade <= 0:
            await ctx.send("Por favor, especifique uma quantidade válida para plantar.")
            return

       
        if user_id in self.user_plant_data:
            last_planted, planted_count = self.user_plant_data[user_id]
            if (current_time - last_planted).total_seconds() < self.plant_cooldown and planted_count >= self.max_plant_per_period:
                retry_after_seconds = self.plant_cooldown - (current_time - last_planted).total_seconds()
                retry_after_minutes = retry_after_seconds / 60
                await ctx.send(f"Você atingiu o limite de plantio. Tente novamente em {retry_after_minutes:.2f} minutos.")
                return

        
        if user_id in self.user_plant_data:
            last_planted, planted_count = self.user_plant_data[user_id]
            if (current_time - last_planted).total_seconds() >= self.plant_cooldown:
               
                self.user_plant_data[user_id] = (current_time, quantidade)
            else:
                self.user_plant_data[user_id] = (last_planted, planted_count + quantidade)
        else:
            self.user_plant_data[user_id] = (current_time, quantidade)

        if self.user_plant_data[user_id][1] > self.max_plant_per_period:
            self.user_plant_data[user_id] = (self.user_plant_data[user_id][0], self.max_plant_per_period)
            await ctx.send(f"Você só pode plantar até {self.max_plant_per_period} morangos a cada 30 minutos.")
            return

        plant_data = self.load_plant_data()
        if user_id in plant_data:
            plant_data[user_id] += quantidade
        else:
            plant_data[user_id] = quantidade

        self.save_plant_data(plant_data)
        
        embed = discord.Embed(
            title="Morangos Plantados",
            description=f"{ctx.author.mention} Você plantou <:emoji_14:1253421914630656020> **{quantidade} morangos com sucesso!** A terra mágica acolhe suas sementes, prometendo uma colheita abundante em breve!",
            color=discord.Color(int('F00000', 16))
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def colher(self, ctx, quantidade: int = 1):
        user_id = str(ctx.author.id)
        plant_data = self.load_plant_data()
        farm_data = self.load_farm_data()
        
        if user_id not in plant_data or plant_data[user_id] < quantidade:
            await ctx.send("Você não plantou morangos suficientes para colher essa quantidade.")
            return

        
        plant_data[user_id] -= quantidade
        if plant_data[user_id] == 0:
            del plant_data[user_id]
        self.save_plant_data(plant_data)

        
        if user_id in farm_data:
            farm_data[user_id] += quantidade
        else:
            farm_data[user_id] = quantidade
        self.save_farm_data(farm_data)
        
        embed = discord.Embed(
            title="Morangos Colhidos",
            description=f"{ctx.author.mention} Você colheu <:emoji_14:1253421914630656020> **{quantidade} morangos com sucesso!** Sua cesta está agora repleta de morangos frescos e suculentos, prontos para serem vendidos no mercado ou saboreados em deliciosas receitas.",
            color=discord.Color(int('F0C100', 16))
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def inventario(self, ctx):
        user_id = str(ctx.author.id)
        farm_data = self.load_farm_data()
        quantidade_morangos = farm_data.get(user_id, 0)
        
        embed = discord.Embed(
            title="Inventário de Morangos",
            description=f"Você possui o total de <:emoji_14:1253421914630656020> **{quantidade_morangos} Morangos.**",
            color=discord.Color(int('FF0032', 16))
        )
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Farm(bot))

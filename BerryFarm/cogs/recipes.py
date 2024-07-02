import discord
from discord.ext import commands
import json
import os

# Dicionário de receitas numeradas
recipes = {
    1: {
        "name": "bolo_de_morango",
        "morangos_necessarios": 5,
        "valor_venda": 20
    },
    2: {
        "name": "torta_de_morango",
        "morangos_necessarios": 10,
        "valor_venda": 40
    },
    3: {
        "name": "sorvete_de_morango",
        "morangos_necessarios": 8,
        "valor_venda": 30
    },
    4: {
        "name": "geleia_de_morango",
        "morangos_necessarios": 6,
        "valor_venda": 25
    },
    5: {
        "name": "suco_de_morango",
        "morangos_necessarios": 4,
        "valor_venda": 15
    },
    6: {
        "name": "salada_de_frutas_com_morangos",
        "morangos_necessarios": 7,
        "valor_venda": 35
    },
    7: {
        "name": "creme_de_morango",
        "morangos_necessarios": 9,
        "valor_venda": 45
    },
    8: {
        "name": "morango_caramelizado",
        "morangos_necessarios": 3,
        "valor_venda": 12
    }
}

class Recipes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='receita')
    async def make_recipe(self, ctx, recipe_number: int):
        user_id = str(ctx.author.id)

        if recipe_number in recipes:
            recipe = recipes[recipe_number]
            recipe_name = recipe['name']
            morangos_necessarios = recipe['morangos_necessarios']

            try:
                with open('fazenda.json', 'r') as f:
                    fazenda = json.load(f)
            except FileNotFoundError:
                fazenda = {}

            # Corrigir leitura dos morangos do usuário
            morangos_usuario = fazenda.get(user_id, 0)

            if morangos_usuario >= morangos_necessarios:
                fazenda[user_id] -= morangos_necessarios

                with open('fazenda.json', 'w') as f:
                    json.dump(fazenda, f, indent=4)

                try:
                    with open('receitas.json', 'r') as f:
                        receitas = json.load(f)
                except FileNotFoundError:
                    receitas = {}

                if user_id not in receitas:
                    receitas[user_id] = {}
                if recipe_name not in receitas[user_id]:
                    receitas[user_id][recipe_name] = 0
                receitas[user_id][recipe_name] += 1

                with open('receitas.json', 'w') as f:
                    json.dump(receitas, f, indent=4)

                embed = discord.Embed(title="Receita Produzida!", color=discord.Color.green())
                embed.add_field(name="Aventura Culinária",
                                value=f'{ctx.author.mention} Produziu a receita **{recipe_name.replace("_", " ").title()}** com sucesso!')
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Receita Falhou", color=discord.Color.red())
                embed.add_field(name="Ingredientes Insuficientes",
                                value=f'{ctx.author.mention}, você não tem morangos suficientes para fazer a receita "{recipe_name.replace("_", " ").title()}". Você precisa de {morangos_necessarios} morangos, você tem apenas {morangos_usuario}.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Receita Não Encontrada", color=discord.Color.orange())
            embed.add_field(name="Erro de Receita",
                            value=f'{ctx.author.mention}, receita não encontrada com o número "{recipe_number}".')
            await ctx.send(embed=embed)

    @commands.command(name='vre')
    async def sell_recipe(self, ctx, recipe_number: int):
        user_id = str(ctx.author.id)

        if recipe_number in recipes:
            recipe = recipes[recipe_number]
            recipe_name = recipe['name']
            valor_venda = recipe['valor_venda']

            try:
                with open('receitas.json', 'r') as f:
                    receitas = json.load(f)
            except FileNotFoundError:
                receitas = {}

            if user_id in receitas and receitas[user_id].get(recipe_name, 0) > 0:
                receitas[user_id][recipe_name] -= 1
                if receitas[user_id][recipe_name] == 0:
                    del receitas[user_id][recipe_name]

                with open('receitas.json', 'w') as f:
                    json.dump(receitas, f, indent=4)

                try:
                    with open('banco.json', 'r') as f:
                        banco = json.load(f)
                except FileNotFoundError:
                    banco = {}

                if user_id not in banco:
                    banco[user_id] = 0
                banco[user_id] += valor_venda

                with open('banco.json', 'w') as f:
                    json.dump(banco, f, indent=4)

                embed = discord.Embed(title="Receita Vendida!", color=discord.Color.gold())
                embed.add_field(name="Sucesso na Venda",
                                value=f'💰 {ctx.author.mention} vendeu a receita "{recipe_name.replace("_", " ").title()}" por {valor_venda} moedas!')
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="Venda Falhou", color=discord.Color.red())
                embed.add_field(name="Receita Não Encontrada",
                                value=f'{ctx.author.mention}, você não tem a receita "{recipe_name.replace("_", " ").title()}" para vender.')
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Receita Não Encontrada", color=discord.Color.orange())
            embed.add_field(name="Erro de Receita",
                            value=f'{ctx.author.mention}, receita não encontrada com o número "{recipe_number}".')
            await ctx.send(embed=embed)

    @commands.command(name='list')
    async def list_recipes(self, ctx):
        embed = discord.Embed(title="Receitas de Morango", color=discord.Color.red())
        for recipe_number, recipe_details in recipes.items():
            description = (
                f"Nome: {recipe_details['name'].replace('_', ' ').title()}\n"
                f"Morangos Necessários: {recipe_details['morangos_necessarios']}\n"
                f"Valor de Venda: {recipe_details['valor_venda']}"
            )
            embed.add_field(name=f"Receita {recipe_number}", value=description, inline=False)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='mre')
    async def list_user_recipes(self, ctx):
        user_id = str(ctx.author.id)
        try:
            with open('receitas.json', 'r') as f:
                receitas = json.load(f)
        except FileNotFoundError:
            receitas = {}

        user_recipes = receitas.get(user_id, {})
        if user_recipes:
            embed = discord.Embed(title="Suas Receitas", color=discord.Color.green())
            for recipe_name, quantity in user_recipes.items():
                embed.add_field(name=recipe_name.replace('_', ' ').title(), value=f'Quantidade: {quantity}', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'{ctx.author.mention}, você não tem receitas armazenadas.')

async def setup(bot):
    await bot.add_cog(Recipes(bot))
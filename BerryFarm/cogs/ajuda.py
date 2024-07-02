import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command(name="ajuda")
    async def ajuda(self, ctx):
        embed = discord.Embed(
            title="Comandos do Bot",
            description="Aqui estão os comandos disponíveis:",
            color=discord.Color(int('FF7800', 16))
        )
        embed.add_field(name="f!plantar [quantidade]", value="Planta a quantidade especificada de morangos. Se não especificar, planta 1 por padrão.", inline=False)
        embed.add_field(name="f!colher [quantidade]", value="Colhe a quantidade especificada de morangos. Se não especificar, colhe 1 por padrão.", inline=False)
        embed.add_field(name="f!vender [quantidade]", value="Vende a quantidade especificada de morangos. Se não especificar, vende todos por padrão.", inline=False)
        embed.add_field(name="f!inventario", value="Mostra quantos morangos você tem no inventário.", inline=False)
        embed.add_field(name="f!saldo", value="Mostra o saldo de dinheiro no banco.", inline=False)
        embed.add_field(name="f!list", value="Apresenta a lista completa das receitas disponíveis.", inline=False)
        embed.add_field(name="f!mre", value="Mostra suas receitas armazenadas.", inline=False)
        embed.add_field(name="f!vre [numero]", value="Vende uma receita específica pelo número correspondente.", inline=False)
        embed.add_field(name="f!receita [numero]", value="Cozinha uma receita específica pelo número correspondente.", inline=False)
        embed.add_field(name="f!ranking", value="Mostra o ranking de membros com mais dinheiro.", inline=False)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))

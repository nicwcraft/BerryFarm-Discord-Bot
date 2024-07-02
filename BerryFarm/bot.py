import discord
from discord.ext import commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True


bot = commands.Bot(command_prefix='f!', intents=intents)

TOKEN = ''


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'cogs.{filename[:-3]} carregado com sucesso.')
            except Exception as e:
                print(f'Erro ao carregar o cog cogs.{filename[:-3]}: {e}')

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    await bot.change_presence(activity=discord.Game(name="f!ajuda"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando não encontrado.')
    else:
        raise error

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())

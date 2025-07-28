import discord
from discord.ext import commands
import asyncio

from auth import TOKEN, GUILD_ID

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.GUILD_ID = GUILD_ID

    async def on_ready(self):
        print(f"Bot conectado como {self.user}")
        
bot = MyBot(command_prefix=["!", "Eli ", "eli ", "eli", "Eli"], intents=intents)

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    try:
        guild = ctx.guild
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        await ctx.send(f"Sincronizado {len(synced)} comandos de barra para este servidor.")
        print(f"Sincronizados {len(synced)} comandos.")
    except Exception as e:
        await ctx.send(f"Falha ao sincronizar: {e}")
        print(e)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    await bot.process_commands(message)

async def main():
    await bot.load_extension("profile.main")
    await bot.load_extension("roles.main")
    await bot.load_extension("anonymous_fax.main")
    await bot.load_extension("interactions.main")
    await bot.load_extension("admin_tools.main")
    await bot.load_extension("dynamic_commands.main") # <-- NOVO MÓDULO CARREGADO

    await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
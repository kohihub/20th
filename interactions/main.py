import discord
import random
from discord.ext import commands

from .gifs import *
from profile import profile_system

class InteractionCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[✅] cog/modulo de Interações carregado.")

    async def _comando_interacao(self, ctx, member: discord.Member, gifs, descricao, acao_passado, tipo):
        if member == ctx.author:
            await ctx.send(f"Está tão carente assim? kkkkkkkkkkkkk", delete_after=10)
            return

        gif = random.choice(gifs)
        
        deu, recebeu = profile_system.increment_interaction_counters(ctx.author.id, member.id, tipo)

        embed = discord.Embed(
            description=f"**{ctx.author.display_name}** {descricao} **{member.display_name}**",
            color=discord.Color.from_rgb(0, 180, 216),
        )
        embed.set_image(url=gif)
        embed.set_footer(
        text=f"{member.display_name} got {acao_passado} {recebeu} times and {ctx.author.display_name} {acao_passado} others {deu} times"        )
        await ctx.send(embed=embed)

    # --- LISTA DE COMANDOS ---

# comando blush
    @commands.command(name="blush")
    async def blush(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, blush_gifs, "is blushing at", "blushed at", "blush")

# Comando Love
    @commands.command(name="love")
    async def love(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, love_gifs, "is showing love to", "loved", "love")

# Comando Boop
    @commands.command(name="boop")
    async def boop(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, boop_gifs, "boops", "booped", "boop")

# Comando Lurk
    @commands.command(name="lurk")
    async def lurk(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, lurk_gifs, "is lurking around", "lurked", "lurk")

# Comando Cheer
    @commands.command(name="cheer")
    async def cheer(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, cheer_gifs, "is cheering up", "cheered", "cheer")

# Comando Nom
    @commands.command(name="nom")
    async def nom(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, nom_gifs, "noms", "nommed", "nom")

# Comando Cuddle
    @commands.command(name="cuddle")
    async def cuddle(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, cuddle_gifs, "is cuddling", "cuddled", "cuddle")

# Comando Nuzzle
    @commands.command(name="nuzzle")
    async def nuzzle(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, nuzzle_gifs, "is nuzzling", "nuzzled", "nuzzle")

# Comando Dance
    @commands.command(name="dance")
    async def dance(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, dance_gifs, "is dancing with", "danced with", "dance")

# Comando Pat
    @commands.command(name="pat")
    async def pat(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, pat_gifs, "is patting", "patted", "pat")

# Comando Feed
    @commands.command(name="feed")
    async def feed(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, feed_gifs, "is feeding", "fed", "feed")

# Comando Peck
    @commands.command(name="peck")
    async def peck(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, peck_gifs, "is pecking", "pecked", "peck")

# Comando Glomp
    @commands.command(name="glomp")
    async def glomp(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, glomp_gifs, "is glomping", "glomped", "glomp")

# Comando Poke
    @commands.command(name="poke")
    async def poke(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, poke_gifs, "is poking", "poked", "poke")

# Comando Handhold
    @commands.command(name="handhold")
    async def handhold(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, handhold_gifs, "is holding hands with", "held hands with", "handhold")

# Comando Pout
    @commands.command(name="pout")
    async def pout(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, pout_gifs, "is pouting at", "pouted at", "pout")

# Comando Happy
    @commands.command(name="happy")
    async def happy(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, happy_gifs, "is happy with", "was happy with", "happy")

# Comando Sleep
    @commands.command(name="sleep")
    async def sleep(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, sleep_gifs, "is sleeping next to", "slept next to", "sleep")

# Comando Highfive
    @commands.command(name="highfive")
    async def highfive(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, highfive_gifs, "gives a high five to", "high-fived", "highfive")

# Comando Thumbsup
    @commands.command(name="thumbsup")
    async def thumbsup(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, thumbsup_gifs, "gives a thumbs up to", "gave a thumbs up to", "thumbsup")

# Comando Hug
    @commands.command(name="hug")
    async def hug(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, hug_gifs, "is hugging", "hugged", "hug")

# Comando Tickle
    @commands.command(name="tickle")
    async def tickle(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, tickle_gifs, "is tickling", "tickled", "tickle")

# Comando Kiss
    @commands.command(name="kiss")
    async def kiss(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, kiss_gifs, "is kissing", "kissed", "kiss")

# Comando Wag
    @commands.command(name="wag")
    async def wag(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, wag_gifs, "is wagging at", "wagged at", "wag")

# Comando Laugh
    @commands.command(name="laugh")
    async def laugh(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, laugh_gifs, "is laughing with", "laughed with", "laugh")

# Comando Wave
    @commands.command(name="wave")
    async def wave(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, wave_gifs, "waves at", "waved at", "wave")

# Comando Lick
    @commands.command(name="lick")
    async def lick(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, lick_gifs, "is licking", "licked", "lick")


# Comando tijolo
    @commands.command(name="brick")
    async def brick(self, ctx, member: discord.Member):
        await self._comando_interacao(ctx, member, brick_gifs, "is launching bricks", "bricked", "brick")


async def setup(bot: commands.Bot):
    await bot.add_cog(InteractionCog(bot))

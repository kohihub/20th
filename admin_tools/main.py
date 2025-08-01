import discord
from discord.ext import commands

CARGO_PERMITIDO_NOME = "Furry" 

class AdminToolsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[✅] cog/modulo de Ferramentas Admin carregado.")


    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRole):
            try:
                await ctx.message.delete()
            except discord.Forbidden:
                pass
            await ctx.send(f"{ctx.author.mention}, Heyyy, você não trabalha aqui para usar esse comando! Quer tanto um emprego assim? Fica no meu lugar então!  ( `ε´ )", ephemeral=True)
        else:
            print(f"[❌] Erro nesse comando: {error}")

    # --- Comandos ---

    @commands.command(name="dizer", aliases=['d'])
    @commands.has_role(CARGO_PERMITIDO_NOME)
    async def say_command(self, ctx: commands.Context, *, mensagem: str):
        
        send_kwargs = {}

        if ctx.message.attachments:
            send_kwargs['file'] = await ctx.message.attachments[0].to_file()
        
        if ctx.message.reference:
            send_kwargs['reference'] = ctx.message.reference

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print(f"[❌] Não foi possível deletar a mensagem de comando em {ctx.channel.name}")

        await ctx.send(mensagem, **send_kwargs)



    @commands.command(name="embed", aliases=['e'])
    @commands.has_role(CARGO_PERMITIDO_NOME)
    async def embed_command(self, ctx: commands.Context, *, mensagem: str):
        
        embed = discord.Embed(
            description=mensagem,
            color=discord.Color.from_str("#00b4d8")
        )

        send_kwargs = {'embed': embed}
        
        if ctx.message.attachments:
            anexo = ctx.message.attachments[0]
            send_kwargs['file'] = await anexo.to_file()
            embed.set_image(url=f"attachment://{anexo.filename}")

        if ctx.message.reference:
            send_kwargs['reference'] = ctx.message.reference

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            print(f"[❌]  Não foi possível deletar a mensagem de comando em {ctx.channel.name}")

        await ctx.send(**send_kwargs)



    @commands.command(name="editar", aliases=['edit'])
    @commands.has_role(CARGO_PERMITIDO_NOME)
    async def edit_command(self, ctx: commands.Context, *, novo_conteudo: str):

        if ctx.message.reference is None:
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.mention}, Heyyy, você precisa respoder a mensagem para eu saber o que editar! aiai, boboca... (>_<)", ephemeral=True)
            return

        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass

        try:
            mensagem_original = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except discord.NotFound:
            await ctx.send("Não consegui encontrar a mensagem que você respondeu... Ela foi deletada?  (×﹏×)", ephemeral=True)
            return

        if mensagem_original.author != self.bot.user:
            await ctx.send("Heyyy bobão, eu só posso editar as minhas mensagens  ┐(‘～` )┌", ephemeral=True)
            return

        try:
            if mensagem_original.embeds:
                embed_original = mensagem_original.embeds[0]
                embed_original.description = novo_conteudo
                await mensagem_original.edit(embed=embed_original)
            else:
                await mensagem_original.edit(content=novo_conteudo)
            
            await ctx.send("Mensagem editada hihihi, ninguém vai saber (>ᴗ•)", ephemeral=True)

        except discord.Forbidden:
            await ctx.send("Eu não posso fazer isso   (¬_¬ )", ephemeral=True)
        except Exception as e:
            print(f"Erro ao editar mensagem: {e}")
            await ctx.send("Eu acho que fiz bagunça...  ヽ(°〇°)ﾉ", ephemeral=True)



async def setup(bot: commands.Bot):
    await bot.add_cog(AdminToolsCog(bot))
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button

# --- Configuração do Módulo ---
CARGO_PERMITIDO_NOME = "Furry" # ❗ Lembre-se de verificar se este é o nome exato do cargo

# --- A View Persistente para o Botão de Remoção ---
class PersistentRemoveRoleView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Remover Cargo", style=discord.ButtonStyle.danger, custom_id="remove_role_button:*")
    async def remove_role_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer(ephemeral=True)
        try:
            role_id = int(interaction.data["custom_id"].split(":")[1])
            role = interaction.guild.get_role(role_id)

            if not role:
                await interaction.followup.send("O cargo associado a este botão não existe mais.", ephemeral=True)
                return

            if role in interaction.user.roles:
                await interaction.user.remove_roles(role, reason="Cargo removido via botão.")
                await interaction.followup.send(f"✅ O cargo **{role.name}** foi removido!", ephemeral=True)
            else:
                await interaction.followup.send(f"Você não possui o cargo **{role.name}**.", ephemeral=True)
        
        except Exception as e:
            print(f"Erro no botão de remover cargo: {e}")
            await interaction.followup.send("Ocorreu um erro ao processar sua solicitação.", ephemeral=True)


# --- O Cog Principal ---
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
            await ctx.send(f"{ctx.author.mention}, Heyyy, você não trabalha aqui para usar esse comando! Quer tanto um emprego assim? Fica no meu lugar então!  ( `ε´ )", delete_after=10)
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
            await ctx.send(f"{ctx.author.mention}, Heyyy, você precisa respoder a mensagem para eu saber o que editar! aiai, boboca... (>_<)", delete_after=10)
            return
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        try:
            mensagem_original = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        except discord.NotFound:
            await ctx.send("Não consegui encontrar a mensagem que você respondeu... Ela foi deletada?  (×﹏×)", delete_after=10)
            return
        if mensagem_original.author != self.bot.user:
            await ctx.send("Heyyy bobão, eu só posso editar as minhas mensagens  ┐(‘～` )┌", delete_after=10)
            return
        try:
            if mensagem_original.embeds:
                embed_original = mensagem_original.embeds[0]
                embed_original.description = novo_conteudo
                await mensagem_original.edit(embed=embed_original)
            else:
                await mensagem_original.edit(content=novo_conteudo)
            await ctx.send("Mensagem editada hihihi, ninguém vai saber (>ᴗ•)", delete_after=5)
        except discord.Forbidden:
            await ctx.send("Eu não posso fazer isso   (¬_¬ )", delete_after=10)
        except Exception as e:
            print(f"Erro ao editar mensagem: {e}")
            await ctx.send("Eu acho que fiz bagunça...  ヽ(°〇°)ﾉ", delete_after=10)

    @commands.command(name="ux_2735_28452")
    @commands.has_permissions(administrator=True)
    async def criar_painel_remocao_prefix(self, ctx: commands.Context):
        ID_DO_CARGO_PARA_REMOVER = 123456789012345678 # ❗ SUBSTITUA PELO ID DO CARGO REAL
        TEXTO_DA_MENSAGEM = "Clique no botão abaixo para deixar de ser Furry."
        TEXTO_DO_BOTAO = "Deixar cargo."
        
        cargo = ctx.guild.get_role(ID_DO_CARGO_PARA_REMOVER)
        if not cargo:
            await ctx.send(f"Cargo não encontrado: `{ID_DO_CARGO_PARA_REMOVER}`", delete_after=15)
            return

        view = PersistentRemoveRoleView()
        button = view.children[0]
        button.label = TEXTO_DO_BOTAO
        button.custom_id = f"remove_role_button:{cargo.id}"
        
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        
        await ctx.channel.send(content=TEXTO_DA_MENSAGEM, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminToolsCog(bot))
    bot.add_view(PersistentRemoveRoleView())
    ID_DO_CARGO_PARA_REMOVER = 123456789012345678 # ❗ SUBSTITUA PELO ID DO CARGO REAL
    TEXTO_DA_MENSAGEM = "Clique no botão abaixo para deixar de ser Furry."
    TEXTO_DO_BOTAO = "Deixar cargo."
        
    cargo = ctx.guild.get_role(ID_DO_CARGO_PARA_REMOVER)
    if not cargo:
            await ctx.send(f"Cargo não encontrado: `{ID_DO_CARGO_PARA_REMOVER}`", delete_after=15)
            return

    view = PersistentRemoveRoleView()
    button = view.children[0]
    button.label = TEXTO_DO_BOTAO
    button.custom_id = f"remove_role_button:{cargo.id}"
        
    try:
            await ctx.message.delete()
    except discord.Forbidden:
            pass
        
    await ctx.channel.send(content=TEXTO_DA_MENSAGEM, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(AdminToolsCog(bot))
    # CORRIGIDO: Adicionada a view para que os botões funcionem após reinicializações
    bot.add_view(PersistentRemoveRoleView())
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


    @commands.command(name="ux_2735_28452")
    @commands.has_permissions(administrator=True)
    async def criar_painel_remocao_prefix(self, ctx: commands.Context):
        
        ID_DO_CARGO_PARA_REMOVER = 123456789012345678
        TEXTO_DA_MENSAGEM = "Clique no botão abaixo para deixar de ser Furry."
        TEXTO_DO_BOTAO = "Deixar cargo."
        
    cargo = ctx.guild.get_role(ID_DO_CARGO_PARA_REMOVER)
    if not cargo:
            await ctx.send(f"Cargo não encontrado: `{ID_DO_CARGO_PARA_REMOVER}`", delete_after=15)
            return

    view = PersistentRemoveRoleView()
    button = view.children[0]
    button.label = TEXTO_DO_BOTAO
    button.custom_id = f"remove_role_button:{cargo.id}"
        
    try:
            await ctx.message.delete()
    except discord.Forbidden:
            pass
        
    await ctx.channel.send(content=TEXTO_DA_MENSAGEM, view=view)




async def setup(bot: commands.Bot):
    await bot.add_cog(AdminToolsCog(bot))
    bot.add_view(PersistentRemoveRoleView())
    

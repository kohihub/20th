import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Modal, TextInput

CARTAS_CANAL_ID = 1382743951454507240


class FaxModal(Modal, title="📠 Enviar Fax Anônimo"):
    destinatario = TextInput(
        label="Para quem é o fax?",
        placeholder="Ex: Felps, Enaldinho, Everson Zoio, ContenteConTV...",
        style=discord.TextStyle.short,
        required=True
    )

    conteudo = TextInput(
        label="Qual a sua mensagem?",
        placeholder="Escreva sua mensagem anônima aqui.",
        style=discord.TextStyle.paragraph,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        destinatario_str = self.destinatario.value
        conteudo_str = self.conteudo.value
        
        canal_de_cartas = interaction.client.get_channel(CARTAS_CANAL_ID)

        if canal_de_cartas:
            embed = discord.Embed(
                title=f"📠 {destinatario_str}, você recebeu um fax anônimo",
                description=conteudo_str,
                color=discord.Color.from_str("#00b4d8")
            )
            await canal_de_cartas.send(embed=embed)
            
            await interaction.response.send_message("Fax enviado com sucesso!  ( ´ ω ` ) ", ephemeral=True)
        else:
            await interaction.response.send_message("Não encontrei o canal para enviar o fax.  (⇀‸↼‶) ", ephemeral=True)


class AnonymousFaxCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[✅] cog/modulo de Fax Anônimo carregado.")

    @app_commands.command(name="fax", description="Envia um fax anônimo para o mural.")
    async def fax(self, interaction: discord.Interaction):
        await interaction.response.send_modal(FaxModal())

async def setup(bot: commands.Bot):
    await bot.add_cog(AnonymousFaxCog(bot))
import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Select

class RoleSelectView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RoleSelect())

class RoleSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Limpar", value="clear_selection", description="Use para limpar sua seleção atual e poder remover um cargo.",emoji="✖️"),
            discord.SelectOption(label="Old Game+", description="Cargo para ser marcado em convite de jogos ou call de jogos em geral.", emoji="🎮"),
            discord.SelectOption(label="League of Legends", description="Que desprezo... Mas tudo bem, é isso que você quer...", emoji="⚔️"),
            discord.SelectOption(label="Balatro", description="Jogo de cartinha, não tem muito o que falar.", emoji="🃏"),
            discord.SelectOption(label="Webfishing", description="Não é Webfisting!!! Parem com isso!", emoji="🐟"),
            discord.SelectOption(label="Stardew Valley", description="Para os fazendeiros.", emoji="🌱"),
            discord.SelectOption(label="Overwatch", description="Vamos?", emoji="🕐"),
            discord.SelectOption(label="Roblox", description="Uh!", emoji="😏"),
            discord.SelectOption(label="Genshin Impact", description="Corre, é gacha!", emoji="💳"),
            discord.SelectOption(label="Dead by Daylight", description="Sem comentários.", emoji="🧟"),
            discord.SelectOption(label="Minecraft", description="Que saudade da primeira seed que tivemos.", emoji="⛏️"),

        ]

        super().__init__(
            placeholder="O que vamos jogar?",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="persistent_role_select"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        selection = self.values[0]
        user = interaction.user

        if selection == "clear_selection":
            await interaction.followup.send("Limpei sua seleção. Agora você pode escolher novamente para adicionar ou remover um cargo.  ( ˙▿˙ )", ephemeral=True)
            return 

        guild = interaction.guild
        role_name = selection
        role = discord.utils.get(guild.roles, name=role_name)

        if role is None:
            print(f"[❌] '{role_name}' não foi encontrado. Criando cargo...")
            try:
                role = await guild.create_role(name=role_name, reason=f"Cargo criado pela Barista.")
                print(f"[✅] Cargo '{role_name}' criado com sucesso.")
            except discord.Forbidden:
                await interaction.followup.send("Preciso de permissão para fazer isso  (＃＞＜)", ephemeral=True)
                return

        if role in user.roles:
            await user.remove_roles(role)
            await interaction.followup.send(f"**{role.name}** foi removido, não vou contar para ninguém que você parou de jogar hihi (=^-ω-^=)", ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.followup.send(f"Agora você faz parte do cargo de **{role.name}**, bom jogo!  (＾▽＾)", ephemeral=True)

        if role in user.roles:
            await user.remove_roles(role)
            await interaction.followup.send(f"**{role.name}** foi removido, não vou contar para ninguém que você parou de jogar hihi (=^-ω-^=)", ephemeral=True)
        else:
            await user.add_roles(role)
            await interaction.followup.send(f"Agora você faz parte do cargo de **{role.name}**, bom jogo!  (＾▽＾)", ephemeral=True)


class RoleCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[✅] cog/modulo de Cargos carregado.")

    @app_commands.command(name="setup_cargos", description="[Admin] Cria.")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_roles(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🎮 O que vamos jogar?",
            description="Utilize para marcar e convidar pessoas que também tenham o mesmo cargo de jogo! ＼(＾▽＾)／\n(Os cargos mudam conforme um jogo se torna relevante ou deixa de ser no servidor.)\nPara deixar de seguir um cargo de jogo é só escolher ele novamente na lista!",
            color=discord.Color.from_rgb(0, 180, 216)
        )
        
        await interaction.channel.send(embed=embed, view=RoleSelectView())
        await interaction.response.send_message("Feito! >.<", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleCog(bot))
    bot.add_view(RoleSelectView())
# reaction_roles/main.py

import discord
from discord.ext import commands
from discord import app_commands
import traceback

from . import database

class ReactionRolesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reaction_config = database.get_reaction_config()
        print("[✅] cog/modulo de Cargos por Reação carregado.")


    @app_commands.command(name="cargo_canal", description="[Admin] Define o canal para a mensagem de cargos por reação.")
    @app_commands.checks.has_permissions(administrator=True)
    async def cargo_canal(self, interaction: discord.Interaction, canal: discord.TextChannel):
        database.set_config_value("channel_id", canal.id)
        self.reaction_config["channel_id"] = canal.id # Atualiza o cache local
        await interaction.response.send_message(f"O canal de reações agora é: {canal.mention} ૮₍ ˶ᵔ ᵕ ᵔ˶ ₎ა", ephemeral=True)

    @app_commands.command(name="cargo_mensagem", description="[Admin] Define a mensagem para os cargos por reação pelo ID.")
    @app_commands.checks.has_permissions(administrator=True)
    async def cargo_mensagem(self, interaction: discord.Interaction, message_id: str):
        try:
            msg_id_int = int(message_id)
            database.set_config_value("message_id", msg_id_int)
            self.reaction_config["message_id"] = msg_id_int # Atualiza o cache
            await interaction.response.send_message(f"A mensagem foi definida pelo id: `{message_id}`.  ⸜(｡˃ ᵕ ˂ )⸝", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Esse ID está errado...  (＞﹏＜)", ephemeral=True)

    @app_commands.command(name="cargo_add", description="[Admin] Adiciona um emoji e um cargo à mensagem configurada.")
    @app_commands.checks.has_permissions(administrator=True)
    async def cargo_add(self, interaction: discord.Interaction, emoji: str, cargo: discord.Role):
        await interaction.response.defer(ephemeral=True)
        
        channel_id = self.reaction_config.get("channel_id")
        message_id = self.reaction_config.get("message_id")
        if not channel_id or not message_id:
            await interaction.followup.send("Heyy! Por favor, configure o canal e a mensagem primeiro, bobão!", ephemeral=True)
            return

        try:
            target_channel = self.bot.get_channel(channel_id)
            target_message = await target_channel.fetch_message(message_id)

            await target_message.add_reaction(emoji)
            
            database.add_role_mapping(emoji, cargo.id)
            
            if "role_mappings" not in self.reaction_config:
                self.reaction_config["role_mappings"] = {}
            self.reaction_config["role_mappings"][emoji] = cargo.id

            await interaction.followup.send(f"O Emoji {emoji} foi adicionado ao cargo: **{cargo.name}**! (  ≧ᗜ≦)", ephemeral=True)

        except discord.NotFound:
            await interaction.followup.send("Não consegui encontrar o canal nem a mensagem :/")
        except discord.Forbidden:
            await interaction.followup.send("Eu não tenho permissão...")
        except Exception as e:
            await interaction.followup.send(f"Algo deu errado, eu não estou bem: {e}")


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        
        if payload.user_id == self.bot.user.id:
            return

        if payload.message_id == self.reaction_config.get("message_id"):
            emoji_str = str(payload.emoji)
            mappings = self.reaction_config.get("role_mappings", {})
            
            if emoji_str in mappings:
                role_id = mappings[emoji_str]
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(role_id)
                member = guild.get_member(payload.user_id)
                
                if role and member:
                    await member.add_roles(role, reason="Cargo por reação")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        print("\n--- Reação Removida ---")
        print(f"ID da Mensagem: {payload.message_id} | ID Configurado: {self.reaction_config.get('message_id')}")

        if payload.message_id == self.reaction_config.get("message_id"):
            print("-> Reação na mensagem correta.")
            emoji_str = str(payload.emoji)
            mappings = self.reaction_config.get("role_mappings", {})
            print(f"-> Emoji: {emoji_str} | Mapeamentos: {mappings}")

            if emoji_str in mappings:
                print("--> Emoji encontrado no mapeamento!")
                role_id = mappings[emoji_str]
                guild = self.bot.get_guild(payload.guild_id)
                role = guild.get_role(role_id)
                member = guild.get_member(payload.user_id)

                print(f"--> Cargo encontrado: {role.name if role else 'NÃO ENCONTRADO'}")
                print(f"--> Membro encontrado: {member.name if member else 'NÃO ENCONTRADO'}")

                if role and member:
                    await member.remove_roles(role, reason="Cargo por reação removido")
                    print("---> Cargo removido com sucesso!")
        print("--- Fim da Verificação ---\n")


async def setup(bot: commands.Bot):
    await bot.add_cog(ReactionRolesCog(bot))
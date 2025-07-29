# imports básicos.

import discord
from discord.ext import commands
from discord import app_commands
import traceback
import os

# Imports dos outros modulos.
from . import profile_system
from . import image_generator


# ínicio ---------- 

# Classe do Cog: Agrupa todos os comandos e eventos do perfil
class ProfileCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        print("[✅] cog/modulo de Perfil carregado.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        leveled_up, user_data = profile_system.update_user_xp(message.author)

        if leveled_up:
            level = user_data['level']

    # Os comandos de Perfil: /perfil, /leaderboard e /give_badge
    @app_commands.command(name="perfil", description="Veja seu perfil e badges.")
    async def perfil(self, interaction: discord.Interaction):
        await interaction.response.defer()

        # --- Bloco de depuração ---
        try:
            print(f"[🔃] Iniciando geração de perfil para {interaction.user.name}")
            user = interaction.user
            
            print("[🔃] Buscando dados do usuário...")
            user_data = profile_system.get_user_data(user.id)
            level = user_data['level']
            xp = user_data['xp']
            xp_needed = profile_system.calculate_xp_for_next_level(level)
            user_badges = user_data.get('badges', [])
            print(f"[✅] Dados encontrados: Nível: {level}, XP: {xp}/{xp_needed} e Badges: {user_badges}.")

            print("[🔃] Gerando imagem do perfil...")
            image_buffer = await image_generator.create_profile_image(
                avatar_url=user.display_avatar.url,
                user_name=user.display_name,
                user_badges=user_badges,
                user_level=level,
                current_xp=xp,
                xp_to_next_level=xp_needed,
        
                
            )
            print("[✅] Imagem gerada com sucesso.")

            print("[🔃] Enviando imagem para o Discord...")
            await interaction.followup.send(file=discord.File(fp=image_buffer, filename="perfil.png"))
            print("[✅] Perfil enviado!")


        except Exception as e:
            print(f"[😭] Encontrei um erro!")
            print(f"ERRO: {e}")
            import traceback
            traceback.print_exc()
            await interaction.followup.send("Pra mim já deu! Estou cansada disso. Não quero fazer! (¬`‸´¬)")
            
    
    @app_commands.command(name="leaderboard", description="O leaderboard de clientes viciados em café.")
    async def leaderboard(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            top_users = profile_system.get_leaderboard(limit=10)

            if not top_users:
                await interaction.followup.send("Ainda não tenho nada pra mostrar, ninguém conversa muito...  (＞﹏＜)")
                return
            
            
            emoji_names = ["gold_coin", "silver_coin", "bronze_coin"] 
            fallback_emojis = ["🥇", "🥈", "🥉"] 
            
            custom_emojis = []
            for i, name in enumerate(emoji_names):
                emoji = discord.utils.get(self.bot.emojis, name=name)
                
                if emoji:
                    custom_emojis.append(str(emoji))
                else:
                    print(f"[❌] Emoji personalizado '{name}' não encontrado. Usando emoji padrão.")
                    custom_emojis.append(fallback_emojis[i])
                    

            embed = discord.Embed(
                title="🌠 Overdose de Café - O leaderboard",
                description="Ranking de clientes ativos da cafeteria (≧◡≦) ♡",
                color=discord.Color.from_rgb(0, 180, 216)
            )

            leaderboard_string = ""

            for i, user_data in enumerate(top_users):
                rank = i + 1
                user_id = int(user_data['id'])
                level = user_data['level']

                user = await self.bot.fetch_user(user_id)
                user_name = user.mention if user else f"See you space cowboy... ({user_id})"

                rank_display = f"`{rank}.`"
                emoji_suffix = f" {custom_emojis[i]}" if i < len(custom_emojis) else ""
                
                leaderboard_string += f"{rank_display} {user_name}"
                leaderboard_string += f" **LVL** `{level}`{emoji_suffix}\n"

            embed.description = leaderboard_string
            embed.set_footer(text=f"Parabéns a todos, só peguem leve no café ☆(>ᴗ•)")

            await interaction.followup.send(embed=embed)

        except Exception as e:
            print(f"[😭] Encontrei um erro ao gerar o leaderboard!")
            print(f"ERRO: {e}")
            traceback.print_exc()
            await interaction.followup.send("Não ando muito bem para fazer isso... (×﹏×)")
            
    @app_commands.command(name="badge", description="Concede uma badge a um usuário.")
    @app_commands.checks.has_permissions(administrator=True)
    async def give_badge(self, interaction: discord.Interaction, user: discord.Member, badge_id: str):
        """
        Args:
            user: O membro que receberá o emblema (•⩊•).
            badge_id: O ID da badge (ex: mario_party).
        """
        try:
            # Verifica se o arquivo da badge existe antes de adicioná-la
            badge_path = os.path.join(os.path.dirname(__file__), "assets", "badges", f"{badge_id}.png")
            if not os.path.exists(badge_path):
                await interaction.response.send_message(f"A badge `{badge_id}` não existe   ╮( ˘ ､ ˘ )╭ \nTenta de novo...", ephemeral=True)
                return

            success = profile_system.add_badge_to_user(user.id, badge_id)

            if success:
                embed = discord.Embed(
                    title="Que legal! Você ganhou um emblema! !(^o^)! ",
                    description=f"**{user.display_name}** recebeu o emblema **{badge_id}**! Veja no seu perfil!\nQue inveja... Eu queria uma também (╥﹏╥)",
                    color=discord.Color.from_rgb(0, 180, 216)
                )
                embed.set_image(url="https://media.discordapp.net/attachments/1385315970557546508/1399106470683086868/excited-anime.gif?ex=6887caf0&is=68867970&hm=d40d2140d398419c69c7f4ccf32be243d9a1047fd7131090dbcb0b5b49dd13a3&=&width=548&height=340")
                
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"{user.display_name} já tem essa... Cada pessoa só pode ter uma por vez!  ┐(︶▽︶)┌", ephemeral=True)

        except Exception as e:
            print(f"[❌] Erro no comando badge: {e}")
            await interaction.response.send_message("Eu não estou muito bem agora...  	(-_-;)", ephemeral=True)
        
            
            
async def setup(bot: commands.Bot):
    await bot.add_cog(ProfileCog(bot), guilds=[discord.Object(id=bot.GUILD_ID)])

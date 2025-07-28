# dynamic_commands/main.py

import discord
from discord.ext import commands, tasks
import json
import os
from datetime import datetime

class DynamicCommandsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        # Caminho robusto para o arquivo JSON, dentro da pasta do módulo
        self.regras_path = os.path.join(os.path.dirname(__file__), "regras.json")
        self.regras = self._carregar_regras()
        
        # Listas para guardar as regras de cada tipo
        self.regras_palavra_chave = []
        self.regras_agendadas = []

        # Processa as regras e prepara os gatilhos
        self._distribuir_regras()
        self._registrar_comandos_prefixo()

        # Inicia a tarefa em segundo plano para mensagens agendadas
        self.verificar_agendamentos.start()
        print("[✅] cog/modulo de Comandos Dinâmicos carregado.")

    def cog_unload(self):
        # Para a tarefa quando o módulo é descarregado
        self.verificar_agendamentos.cancel()

    def _carregar_regras(self):
        try:
            with open(self.regras_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _distribuir_regras(self):
        """Separa as regras em listas para otimizar as verificações."""
        for regra in self.regras:
            tipo = regra.get("ativador", {}).get("tipo")
            if tipo == "password":
                self.regras_palavra_chave.append(regra)
            elif tipo == "time":
                self.regras_agendadas.append(regra)

    # --- Métodos Helper Internos ---
    async def _verificar_condicoes(self, message_or_context, condicoes):
        author = getattr(message_or_context, 'author', None)
        channel = getattr(message_or_context, 'channel', None)

        if not author or not channel:
            return False

        for cond in condicoes:
            tipo = cond.get("tipo")
            valor = str(cond.get("id"))
            if tipo == "canal" and str(channel.id) != valor:
                return False
            elif tipo == "cargo" and not any(str(role.id) == valor for role in author.roles):
                return False
            elif tipo == "membro" and str(author.id) != valor:
                return False
        return True

    async def _executar_efeito(self, destino, efeito, args=None):
        tipo = efeito.get("tipo")
        conteudo = efeito.get("conteudo", "")
        
        try:
            if tipo == "mensagem":
                await destino.send(conteudo)
            elif tipo == "mensagem_usuario":
                await destino.send(args if args else "(＃￣0￣)  |  Escreva algo boboca.")
            elif tipo == "embed":
                embed = discord.Embed.from_dict(conteudo)
                await destino.send(embed=embed)
            elif tipo == "embed_usuario":
                embed = discord.Embed(description=args or "(＃￣0￣)  |  Escreva algo boboca.", color=discord.Color.green())
                await destino.send(embed=embed)
        except Exception as e:
            print(f"Erro ao executar efeito: {e}")

    # --- Lógica para criar comandos de prefixo dinamicamente ---
    def _criar_callback_prefixo(self, regra):
        """Cria a função que será executada pelo comando."""
        async def comando_dinamico(ctx, *, args=None):
            if await self._verificar_condicoes(ctx, regra.get("condicoes", [])):
                await self._executar_efeito(ctx.channel, regra.get("efeito"), args)
            else:
                await ctx.send("⚠️ Você não tem permissão para usar este comando.", delete_after=10)
        return comando_dinamico

    # Em dynamic_commands/main.py

    def _registrar_comandos_prefixo(self):
        """Lê as regras e cria os comandos de prefixo."""
        for regra in self.regras:
            ativador = regra.get("ativador", {})
            if ativador.get("tipo") == "prefixo":
                nome_comando = ativador.get("valor", "")
                
                # --- CÓDIGO CORRIGIDO ---
                # Verifica cada prefixo da lista e remove o que encontrar
                for prefix in self.bot.command_prefix:
                    if nome_comando.startswith(prefix):
                        nome_comando = nome_comando[len(prefix):] # Remove o prefixo
                        break # Para no primeiro que encontrar
                
                if nome_comando in self.bot.all_commands:
                    print(f"[ℹ️] Comando de prefixo '{nome_comando}' já existe, pulando.")
                    continue

                callback = self._criar_callback_prefixo(regra)
                comando = commands.Command(callback, name=nome_comando)
                self.bot.add_command(comando)
                print(f"[➕] Comando de prefixo '{nome_comando}' criado dinamicamente.")

    # --- Listener para palavras-chave ---
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        for regra in self.regras_palavra_chave:
            palavra = regra.get("ativador", {}).get("valor", "").lower()
            if palavra and palavra in message.content.lower():
                if await self._verificar_condicoes(message, regra.get("condicoes", [])):
                    await self._executar_efeito(message.channel, regra.get("efeito"))

    # --- Task para mensagens agendadas ---
    @tasks.loop(seconds=60)
    async def verificar_agendamentos(self):
        agora = datetime.now().strftime("%H:%M")
        for regra in self.regras_agendadas:
            horario_regra = regra.get("ativador", {}).get("valor")
            if horario_regra == agora:
                print(f"[⏰] Ativando regra agendada para as {agora}.")
                # Verifica a condição no canal especificado na regra
                condicoes = regra.get("condicoes", [])
                canal_id = next((c['id'] for c in condicoes if c['tipo'] == 'canal'), None)
                if canal_id:
                    canal = self.bot.get_channel(int(canal_id))
                    if canal:
                        await self._executar_efeito(canal, regra.get("efeito"))

    @verificar_agendamentos.before_loop
    async def before_verificar_agendamentos(self):
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot):
    await bot.add_cog(DynamicCommandsCog(bot))
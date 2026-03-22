import asyncio
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from modules.mongodb_conncetion import MongoDBConnectionHandler

load_dotenv()

db = MongoDBConnectionHandler().valid_connection()['result_forms']
colecao = db['result_users']

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

bot_loop = None
CANAL_ID = 1485285844292997152

@bot.event
async def on_ready():
    global bot_loop
    bot_loop = asyncio.get_event_loop()  # ✅ captura o loop aqui
    print(f"✅ Bot online como {bot.user}")


async def enviar_discord(documento: dict):
    canal = bot.get_channel(CANAL_ID)
    if canal is None:
        print("❌ Canal não encontrado.")
        return

    embed = discord.Embed(
        title="📋 Nova Candidatura de Player RP",
        description=f"**{documento.get('name')}** quer entrar no servidor!",
        color=discord.Color.gold()
    )
    embed.add_field(name='👤 Nome',           value=documento.get('name', '—'),        inline=True)
    embed.add_field(name='🎂 Idade',          value=documento.get('age', '—'),         inline=True)
    embed.add_field(name='🎮 Nick',           value=documento.get('nick', '—'),        inline=True)
    embed.add_field(name='💬 Discord',        value=documento.get('discord', '—'),     inline=True)
    embed.add_field(name='🆔 Server ID',      value=documento.get('server_id', '—'),   inline=True)
    embed.add_field(name='⭐ Experiência',    value=documento.get('exp', '—'),         inline=True)
    embed.add_field(name='📖 Histórico',      value=documento.get('hist', '—'),        inline=True)
    embed.add_field(name='🎲 RDM',            value=documento.get('rdm', '—'),         inline=True)
    embed.add_field(name='🚗 VDM',            value=documento.get('vdm', '—'),         inline=True)
    embed.add_field(name='🎭 PG',             value=documento.get('pg', '—'),          inline=True)
    embed.add_field(name='🎯 Meta',           value=documento.get('meta', '—'),        inline=True)
    embed.add_field(name='🚘 Car Jacking',    value=documento.get('car_jacking', '—'), inline=True)
    embed.add_field(name='🏄 Surf',           value=documento.get('surf', '—'),        inline=True)
    embed.add_field(name='📅 Disponibilidade',value=documento.get('disp', '—'),        inline=True)
    embed.add_field(name='\u200b',            value='\u200b',                          inline=True)
    embed.add_field(name='❓ Questão 1',      value=documento.get('q1', '—'),          inline=False)
    embed.add_field(name='❓ Questão 2',      value=documento.get('q2', '—'),          inline=False)
    embed.add_field(name='❓ Questão 3',      value=documento.get('q3', '—'),          inline=False)
    embed.add_field(name='❓ Questão 4',      value=documento.get('q4', '—'),          inline=False)
    embed.add_field(name='❓ Questão 5',      value=documento.get('q5', '—'),          inline=False)
    embed.add_field(name='❓ Questão 6',      value=documento.get('q6', '—'),          inline=False)
    embed.set_footer(text=f"ID: {documento.get('_id')} • ✅ aprovar  ❌ recusar")
    embed.timestamp = discord.utils.utcnow()

    msg = await canal.send(embed=embed)
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")
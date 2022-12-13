import discord
from discord.ext import commands
import random
from main import db
import datetime
import asyncio
import json

class Backup(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def backup(self, ctx):
        cursor = db.cursor()
        await ctx.reply('ok', mention_author=False)

    @commands.command()
    async def backuprestore(self, ctx):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM backups WHERE guild_id='{ctx.guild.id}'")
        result = cursor.fetchall()
        data = json.loads(result[0][1].replace("'", '"').replace('None', '"None"').replace('True', '"True"').replace('False', '"False"'))
        await ctx.guild.edit(name=data['name'], description=data['description'].replace("None", ""), region=data['region'], afk_timeout=data['afk_timeout'], preferred_locale=data['preferred_locale'], reason="Radon Backup Rendszer")
        for em in data['emojis']:
            with open(f"/var/www/cdn/backups/emojis/{ctx.guild.id}/{em.name}.png", "rb") as emoji_img:
                await ctx.guild.create_custom_emoji(name=em.name, image=emoji_img, reason="Radon Backup Rendszer")
        await ctx.reply('ok', mention_author=False)

def setup(client):
    client.add_cog(Backup(client))

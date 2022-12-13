import discord
from discord.ext import commands
import time
import datetime
import asyncio
import requests
import json
from gtts import gTTS
import os
from discord.utils import get
from discord.errors import ClientException
from io import BytesIO
from tempfile import TemporaryFile
import mysql.connector as myc
from main import db
import random
from discord_components import DiscordComponents, Button, ButtonStyle, InteractionType

ffmpeg_options = {
    'options': '-vn'
}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn -reconnect 1'}

class Update(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["emojisteal", "forkemoji", "emojifork", "fork_emoji"], usage=",stealemoji [emoji neve]")
    async def stealemoji(self, ctx, emojiname):
        if ctx.author.guild_permissions.manage_emojis == False:
            perm = "Emotikonok kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return
        emojilist = []
        for i in self.client.guilds:
            emoji = discord.utils.get(i.emojis, name=emojiname)
            if emoji is not None:
                emojilist.append(emoji)
        if len(emojilist)==0:
            await ctx.send("Nem található ilyen emoji!")
            return
        for x in range(len(emojilist)):
            embed=discord.Embed(description="Ezt az emojit keresed? (`igen`/`nem`/`következő`)", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Emoji neve", value=emojilist[x].name)
            embed.add_field(name="Emoji", value=str(emojilist[x]))
            embed.add_field(name="Emoji ID", value=emojilist[x].id)
            embed.add_field(name="Animált?", value="Igen" if emojilist[x].animated else "Nem")
            embed.add_field(name="Emoji szervere", value=emojilist[x].guild)
            embed.add_field(name="Emoji URL", value=emojilist[x].url)
            embed.set_author(name="Emoji lopás", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Emoji lopás", icon_url=self.client.user.avatar_url)
            await ctx.reply(content=f"Összesen **{len(emojilist)}** emojit találtam.", embed=embed, mention_author=False)
            def check(m): return m.author == ctx.author and m.channel == ctx.channel
            cuccxd = 0
            try: msg = await self.client.wait_for("message", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Nem válaszoltál időben!")
                break
            if msg.content == "igen".lower():
                await ctx.guild.create_custom_emoji(name=emojilist[x].name, image=await emojilist[x].url.read(), roles=None, reason=f"Emoji steal - {ctx.author.name}")
                await msg.reply("Az emoji sikeresen hozzá lett adva a szerverhez!", mention_author=False)
                break
            elif msg.content == "nem".lower():
                await msg.reply("Az emoji lopó bezárul.", mention_author=False)
                break
            elif msg.content == "következő".lower():
                cuccxd += 1
                if cuccxd == len(emojilist): await ctx.send("Összesen ennyi emojit találtam!"); break
                else: continue
            else:
                await msg.reply("Helytelen válasz! Az emoji lopó bezárul.", mention_author=False)
                break

    @commands.command()
    async def embedbuilder(self, ctx):
        if ctx.author.guild_permissions.manage_channels==False:
            perm = "Csatornák kezelése."
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return
        try:
            await ctx.send("Minden kérdésre fél perced lesz válaszolni. A válaszokat a chatbe, prefix __nélkül__ írd!")
            kerdesek = ["Melyik csatornába küldjem az embedet?",
                        "Mi legyen a cím?",
                        "Mi legyen a leírás?",
                        "Mi legyen a fejléc/author? (Ha nincs, írd be, hogy `nincs`)",
                        "Mi legyen a lábléc/footer? (Ha nincs, írd be, hogy `nincs`)",
                        "Mi legyen a fejléc ikonja? (Ha nincs, írd be, hogy `nincs`)",
                        "Mi legyen a lábléc ikonja? (Ha nincs, írd be, hogy `nincs`)",
                        "Legyen időbélyeg? (`igen`/`nem`)"]
            valaszok = []
            def check(m): return m.author == ctx.author and m.channel == ctx.channel
            for i in kerdesek:
                await ctx.send(i)
                try:
                    msg = await self.client.wait_for('message', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Nem válaszoltál időben, az embed készítő bezárul.')
                    return
                else: 
                    valaszok.append(msg.content)
            try:
                channel_id = int(valaszok[0][2:-1])
            except:
                await ctx.send(f"Hibás csatornaformátum! Használj {ctx.channel.mention}-t!")
                return
            author = False if valaszok[3] == "nincs" else True
            footer = False if valaszok[4] == "nincs" else True
            aicon = False if valaszok[5] == "nincs" else True
            ficon = False if valaszok[6] == "nincs" else True
            if aicon == True and author == False: await ctx.send("Nem lehet fejléc ikon fejléc nélkül!"); return
            if ficon == True and footer == False: await ctx.send("Nem lehet lábléc ikon lábléc nélkül!"); return
            if valaszok[7] == "igen": timestamp=True
            elif valaszok[7] == "nem": timestamp=False
            else: await ctx.send("Hibás válasz! Lehetőségek: `igen`, `nem`"); return
            channel = self.client.get_channel(channel_id)
            embed=discord.Embed(title=valaszok[1], description=valaszok[2], timestamp=datetime.datetime.utcnow() if timestamp else discord.Embed.Empty, color=0xff9900)
            if author and aicon: embed.set_author(name=valaszok[3], icon_url=valaszok[5])
            if footer and ficon: embed.set_footer(text=valaszok[4], icon_url=valaszok[6])
            if author and not aicon: embed.set_author(name=valaszok[3])
            if footer and not ficon: embed.set_footer(text=valaszok[4])
            await channel.send(embed=embed)
        except:
            raise


    @commands.command()
    async def shards(self, ctx):
        shard1ping = round(self.client.shards[0].latency * 1000)
        shard2ping = round(self.client.shards[1].latency * 1000)
        shard3ping = round(self.client.shards[2].latency * 1000)
        shard4ping = round(self.client.shards[3].latency * 1000)
        shard1guilds = 0
        shard2guilds = 0
        shard3guilds = 0
        shard4guilds = 0
        for guild in self.client.guilds:
            if guild.shard_id == 0:
                shard1guilds = shard1guilds + 1
            if guild.shard_id == 1:
                shard2guilds = shard2guilds + 1
            if guild.shard_id == 2:
                shard3guilds = shard3guilds + 1
            if guild.shard_id == 3:
                shard4guilds = shard4guilds + 1

        embed = discord.Embed(description=f"Ez a szerver a **{ctx.guild.shard_id + 1}.** Shardon található", color=0xFF9900)
        embed.set_author(name="Shard információk", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Shards", icon_url=self.client.user.avatar_url)

        embed.add_field(name="#1 Shard", value=f"Ping: {shard1ping}ms\nSzerverek száma: {shard1guilds}", inline=False)
        embed.add_field(name="#2 Shard", value=f"Ping: {shard2ping}ms\nSzerverek száma: {shard2guilds}", inline=False)
        embed.add_field(name="#3 Shard", value=f"Ping: {shard3ping}ms\nSzerverek száma: {shard3guilds}", inline=False)
        embed.add_field(name="#4 Shard", value=f"Ping: {shard4ping}ms\nSzerverek száma: {shard4guilds}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=["szakma", "munkák", "ajánlottmunka", "meló"])
    async def melo(self, ctx):
        joslatok = ['`Vadász`','`Halász`','`Rendőr`','`Tűzoltó`','`Orvos`','`Gyógyszerész`','`Kamionos`','`Árúszállító`','`Autószerelő`','`Pincér`','`Szakács`','`Étterem tulajdonos`','`Gyári munkás`','`Közgazdász`','`Állattenyésztő`']
        embed = discord.Embed(title="Ajánlott szakma", timestamp=datetime.datetime.utcnow(), color=0xe9b603)
        embed.add_field(name="Neked ajánlott szakma:", value=f"{random.choice(joslatok)}")
        embed.set_author(name="Ajánlás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Ajánlás", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)


def setup(client):
    client.add_cog(Update(client))

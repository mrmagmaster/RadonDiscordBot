import discord
from discord.ext import commands
import time
import datetime
import random
import aiohttp
import platform
import os
import psutil
import urllib
import io
from contextlib import redirect_stdout
import textwrap
import traceback
import mysql.connector as myc
import asyncio
import requests
import bs4
from discord_components import *
from discord.ext import tasks
import mysql.connector as myc
from main import db
dateT = datetime.datetime.utcnow()
panel_msg_id = 0

class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["fekudj", "feküdj"], usage=",fekszik [@említés]")
    async def fekszik(self, ctx, member: discord.Member):
        if member == ctx.author:
            await ctx.reply("Magadat akarod elküldeni aludni? :(", mention_author=False)
            return
        embed = discord.Embed(description=f"{ctx.author.mention} elküldte {member.mention} felhasználót aludni!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Fekszik", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Fekszik", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["ei", "einfo", "emojii", "emoteinfo"], usage=",emojiinfo [emoji (alap discordos emojit a bot nem fogad el)]")
    async def emojiinfo(self, ctx, emoji: discord.Emoji):
        try: emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.NotFound: return await ctx.reply("Nem találtam ilyen emojit.", mention_author=False)
        is_managed = "Igen" if emoji.managed else "Nem"
        is_animated = "Igen" if emoji.animated else "Nem"
        embed=discord.Embed(color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Név", value=f"`{emoji.name}`")
        embed.add_field(name="ID", value=f"{emoji.id}")
        embed.add_field(name="Letöltés", value=f"**[Kattints ide!]({emoji.url})**")
        embed.add_field(name="Dátum", value=f"{emoji.created_at.strftime('%Y. %m. %d. @ %H:%M:%S')}")
        embed.add_field(name="Feltöltötte", value=f"{emoji.user.mention} (**{emoji.user}**)")
        embed.add_field(name="Formátum", value=f"`<:{emoji.name}:{emoji.id}>`")
        embed.add_field(name="Animált?", value=f"{is_animated}")
        embed.add_field(name="Kezelt?", value=f"{is_managed}")
        embed.set_author(name="Emojiinfo", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Emojiinfo", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=emoji.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.client.process_commands(after)

    @commands.command()
    async def allzene(self, ctx):
        await ctx.reply(f"**{len(self.client.voice_clients)}** hangcsatornán játszok zenét jelenleg!", mention_author=False)

    @commands.command(usage=",covid [ország neve angolul]", aliases=["koronavírus", "koronavirus"])
    async def covid(self, ctx, *, countryName = None):
        try:
                url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
                stats = requests.get(url)
                json_stats = stats.json()
                country = json_stats["country"]
                totalCases = json_stats["cases"]
                todayCases = json_stats["todayCases"]
                totalDeaths = json_stats["deaths"]
                todayDeaths = json_stats["todayDeaths"]
                recovered = json_stats["recovered"]
                active = json_stats["active"]
                critical = json_stats["critical"]
                casesPerOneMillion = json_stats["casesPerOneMillion"]
                deathsPerOneMillion = json_stats["deathsPerOneMillion"]
                totalTests = json_stats["totalTests"]
                testsPerOneMillion = json_stats["testsPerOneMillion"]
                embed2 = discord.Embed(title=f"**Koronavírus a következő országban: {country}**!", description="Az API csak és kizárolag az angol nevű országokat támogatja!", colour=0x0000ff, timestamp=ctx.message.created_at)
                embed2.add_field(name="**Összes eset**", value=totalCases, inline=True)
                embed2.add_field(name="**Új esetek**", value=todayCases, inline=True)
                embed2.add_field(name="**Összes halott**", value=totalDeaths, inline=True)
                embed2.add_field(name="**Új halottak**", value=todayDeaths, inline=True)
                embed2.add_field(name="**Gyógyultak**", value=recovered, inline=True)
                embed2.add_field(name="**Aktív fertőzöttek**", value=active, inline=True)
                embed2.add_field(name="**Korházban ápoltak**", value=critical, inline=True)
                embed2.add_field(name="**Mintavételek**", value=totalTests, inline=True)
                embed2.add_field(name="**Fertőzések egy millió emberből**", value=casesPerOneMillion, inline=True)
                embed2.add_field(name="**Halálesetek egy millió emberből**", value=deathsPerOneMillion, inline=True)
                embed2.add_field(name="**Tesztek egy millió emberből**", value=testsPerOneMillion, inline=True)
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.reply(embed=embed2)
        except:
            embed3 = discord.Embed(colour=0xff0000, timestamp=ctx.message.created_at)
            embed3.set_author(name="Az API nem támogatja az országot!", icon_url=ctx.author.avatar_url)
            embed3.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed3)

    @commands.command(usage=",timer [idő (másodpercben)]", aliases=["time", "cdown", "countdown", "cd", "countd", "visszaszámláló", "visszaszamlalo"])
    async def timer(self, ctx, time: float):
        embed = discord.Embed(color=0xFF9900, footer="Radon × Timer", description=f"A {time} másodperces visszaszámláló elindult!")
        embed2 = discord.Embed(color=0xFF9900, footer="Radon × Timer", description=f"A visszaszámláló lejárt!")
        embed.set_author(name="Visszaszámláló", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Time", icon_url=self.client.user.avatar_url)
        embed2.set_author(name="Visszaszámláló", icon_url=ctx.author.avatar_url)
        embed2.set_footer(text=f"{ctx.author.name} × Time", icon_url=self.client.user.avatar_url)
        msg = await ctx.reply(embed=embed, mention_author=False)
        await asyncio.sleep(time)
        await msg.edit(embed=embed2)
        await ctx.send(ctx.author.mention)

    @commands.command(aliases=["támogatás"])
    async def donate(self, ctx):
        embed = discord.Embed(description="[Tovább a támogatáshoz!](https://paypal.me/scopsyyt)\nMit kapsz érte? :thinking:\n - Támogató rang a support szerveren (leakek csatorna és külön chat)\n - Saját parancs\n - Saját emoji!", color=0xff0099)
        embed.set_author(name="Támogatás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Támogatás", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["parancsok", "segítség", "commands", "cmd"])
    async def help(self, ctx, kategoria=None):
        embed=discord.Embed(color=0xe9b603, footer="Radon × Help", timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Parancsok", value="**[Kattints ide](https://radonbot.hu/commands)**", inline=False)
        embed.add_field(name="Weboldal", value="**[Kattints ide](https://radonbot.hu/)**", inline=True)
        embed.add_field(name="Discord szerver", value="**[Kattints ide](https://discord.gg/d5MH5thSVV)**", inline=False)
        embed.add_field(name="Bot meghívás", value="**[Kattints ide](https://invite.radonbot.hu/)**", inline=True)
        embed.set_author(name="Parancsok", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Help", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["botinfo", "bot-info", "binfo", "bi", "boti"])
    async def botinfó(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        channelCount = len(set(self.client.get_all_channels()))
        embed = discord.Embed(description="A Radon bot információi", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Bot neve", value="Radon", inline=True)
        embed.add_field(name="Készült", value="2021.02.03", inline=True)
        embed.add_field(name="Programozási könytár", value="discord.py")
        embed.add_field(name="Szerverek", value=f"{serverCount}")
        embed.add_field(name="Csatornák", value=f"{channelCount}")
        embed.add_field(name="Felhasználók", value=f"{memberCount}")
        embed.add_field(name="Python verzió", value=f"{pythonVersion}")
        embed.add_field(name="Parancsok száma", value=f"{len(self.client.commands)}")
        embed.add_field(name="discord.py verzió", value=f"{dpyVersion}")
        embed.add_field(name="Operációs rendszer", value=f"Debian 10")
        embed.add_field(name="CPU-k típusa", value="Intel® Xeon® X5650")
        embed.add_field(name="CPU-k száma", value=f"{psutil.cpu_count()} db")
        embed.add_field(name="CPU-k teljesítménye", value="2.67GHz")
        embed.add_field(name="Memória mérete", value=f"4 GB")
        embed.add_field(name="CPU kihasználtság", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="Memória kihasználtság", value=f"{psutil.virtual_memory().percent}%")
        embed.set_author(name="Bot információi", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Bot infók", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)
            
    @commands.command(aliases=["allmember", "össztag", "members", "tagok", "tag"])
    async def alltag(self, ctx):
        embed = discord.Embed(description=f"A bot **{len(set(self.client.get_all_members()))}** felhasználót menedzsel!", timestamp=datetime.datetime.utcnow(), color=0xFF9900)
        embed.set_author(name="Felhasználók", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Felhasználók", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["javaslat", "javasol", "otlet", "suggestion", "suggest"], usage=",ötlet [szöveg]")
    @commands.cooldown(1, 600, type=commands.BucketType.user)
    async def ötlet(self, ctx, *, message1):
        channel = self.client.get_channel(856402092407521310)
        await ctx.reply("<:radon_pipa:811191514369753149> Sikeresen elküldtem a javaslatod!", mention_author=False)
        embed = discord.Embed(description=f"```{message1}```", color=0x0f3f)
        embed.set_author(name="Javaslat", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Javaslat", icon_url=self.client.user.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        message = await channel.send(embed=embed)
        await message.add_reaction('<:radon_check:856423841612824607>')
        await message.add_reaction('<:radon_x:856423841667743804>')

    @commands.Cog.listener()
    async def on_ready(self):
        global start_ido
        start_ido = time.time()
        await asyncio.sleep(10)
        channel = self.client.get_channel(856617292506464277)
        await channel.purge(limit=1)
        embed = discord.Embed(color=0xff9900, timestamp=dateT)
        embed.set_author(name="Radon Vezérlőpanel", icon_url='https://cdn.radonbot.hu:800/images/icon/icon.webp')
        embed.set_footer(text="Radon × Vezérlés", icon_url='https://cdn.radonbot.hu:800/images/icon/icon.webp')
        embed.add_field(name="Szerverek", value=len(self.client.guilds))
        mem = 0
        for guild in self.client.guilds:
            mem = mem + guild.member_count
        embed.add_field(name="Felhasználók", value=mem)
        embed.add_field(name="Ping", value=round(self.client.latency * 1000))
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
        embed.add_field(name="Shardok", value=f"Shard #1 - Ping: `{round(self.client.shards[0].latency * 1000)}ms` - Szerverek: {shard1guilds}\nShard #2 - Ping: `{round(self.client.shards[1].latency * 1000)}ms` - Szerverek: {shard2guilds}\nShard #3 - Ping: `{round(self.client.shards[2].latency * 1000)}ms` - Szerverek: {shard3guilds}\nShard #4 - Ping: `{round(self.client.shards[3].latency * 1000)}ms` - Szerverek: {shard4guilds}")
        message = await channel.send(embed=embed, components=[
            [
                Button(style=ButtonStyle.gray, label="Bot Leállítása"),
                Button(style=ButtonStyle.gray, label="Bot Újraindítása"),
                Button(style=ButtonStyle.green, label="Teljes Újraindítás")
            ],
            [
                Button(style=ButtonStyle.blue, label="Web Leállítása"),
                Button(style=ButtonStyle.blue, label="Web Újraindítása"),
                Button(style=ButtonStyle.red, label="VPS Újraindítása"),
            ],
            [
                Button(style=ButtonStyle.gray, label="Shard 1 Újraindítása"),
                Button(style=ButtonStyle.gray, label="Shard 2 Újraindítása"),
                Button(style=ButtonStyle.gray, label="Shard 3 Újraindítása"),
                Button(style=ButtonStyle.gray, label="Shard 4 Újraindítása")
            ]
        ])
        panel_msg_id = message.id

    @commands.command(usage=",servericon", aliases=["sicon", "gicon", "guildpfp", "spfp", "serverpfp"])
    async def guildicon(self, ctx):
        embed = discord.Embed(title="Szerver Ikon", footer="Radon × Server Icon", description=f"{ctx.guild.name} szerver ikonja", color=0xff9900)
        embed.set_image(url = ctx.guild.icon_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["av", "pfp"], usage=",avatar [@felhasználó]")
    async def avatar(self, ctx, member : discord.Member=None):
        member = ctx.author if not member else member
        embed2 = discord.Embed(title=f"{member} profilképe", color=member.color, timestamp=datetime.datetime.utcnow())
        embed2.set_image(url=member.avatar_url)
        await ctx.reply(embed=embed2, mention_author=False)

    @commands.command(aliases=['chinfo', 'cinfo'], usage=",chinfo (csatorna)")
    async def channelinfo(self, ctx, channel: discord.TextChannel=None):
        channel = ctx.channel or channel
        embed = discord.Embed(description=f"{'Kategória: {}'.format(channel.category.name) if channel.category else 'Nincs kategóriában'}", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"Csatorna Információi ({channel.name})", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author} × Channel Info", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Szervere neve", value=ctx.guild.name, inline=True)
        embed.add_field(name="Csatorna ID", value=channel.id, inline=True)
        a = "Igen" if channel.is_news() else "Nem"
        b = "Igen" if channel.is_nsfw() else "Nem"
        if channel.topic:
            embed.add_field(name="Csatorna Téma", value=f"{channel.topic}", inline=True)
        embed.add_field(name="Csatorna Pozíciója", value=channel.position, inline=True)
        embed.add_field(name="Csatorna Lassítása", value=channel.slowmode_delay, inline=True)
        embed.add_field(name="NSFW csatorna?", value=a, inline=True)
        embed.add_field(name="Bejelentési csatorna?", value=b, inline=True)
        embed.add_field(name="Csatorna létrehozási ideje", value=channel.created_at, inline=True)
        embed.add_field(name="Csatorna Hash", value=hash(channel), inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_button_click(self, res):
        if res.component.label == "Bot Leállítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Bot Leállítása...")
            print("Parancsfájlok kitöltése...")
            for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.client.unload_extension(f"cogs.{filename[:-3]}")
            print("MySQL kapcsolat bezárása...")
            db.close()
            print("Kijelentkezés...")
            await self.client.logout()
        elif res.component.label == "Bot Újraindítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Bot Újraindítása...")
            print("Parancsfájlok kitöltése...")
            for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.client.unload_extension(f"cogs.{filename[:-3]}")
            print("MySQL kapcsolat bezárása...")
            db.close()
            print("Kijelentkezés...")
            await self.client.logout()
            os.system('tmux send-keys "python3 main.py" ENTER')
        elif res.component.label == "Web Leállítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Web Leállítása...")
            os.system('systemctl stop nginx')
        elif res.component.label == "Web Újraindítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Web Újraindítása...")
            os.system('systemctl stop nginx')
            os.system('systemctl start nginx')
        elif res.component.label == "Teljes Újraindítás":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Újraindítás...")
            os.system('systemctl stop mysql')
            os.system('systemctl start mysql')
            os.system('systemctl stop nginx')
            os.system('systemctl start nginx')
            os.system('systemctl stop apache2')
            os.system('systemctl start apache2')
            for filename in os.listdir('./cogs'):
                    if filename.endswith('.py'):
                        self.client.unload_extension(f"cogs.{filename[:-3]}")
            await self.client.logout()
            os.system('tmux send-keys "python3 main.py" ENTER')
        elif res.component.label == "VPS Újraindítás":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> VPS Újraindítása...")
            os.system('reboot')
        elif res.component.label == "Shard 1 Újraindítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Shard 1 Újraindítása...")
            await self.client.shards[0].disconnect()
            await self.client.shards[0].connect()
        elif res.component.label == "Shard 2 Újraindítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Shard 2 Újraindítása...")
            await self.client.shards[1].disconnect()
            await self.client.shards[1].connect()
        elif res.component.label == "Shard 3 Újraindítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Shard 3 Újraindítása...")
            await self.client.shards[2].disconnect()
            await self.client.shards[2].connect()
        elif res.component.label == "Shard 4 Újraindítása":
            await res.respond(type=InteractionType.ChannelMessageWithSource, content=f"<:radon_toltes:811192219579056158> Shard 4 Újraindítása...")
            await self.client.shards[3].disconnect()
            await self.client.shards[3].connect()

    @commands.command(aliases=["bug", "bugreport", "hibareport", "hibajelentes", "hibajelentés"], usage=",hiba [szöveg (FIGYELEM: írd le a hibát, hogy mikor vetted észre, hogy hogyan idézted elő!)]")
    @commands.cooldown(1, 300, type=commands.BucketType.user)
    async def hiba(self, ctx, *, message1):
        channel = self.client.get_channel(856408830623219722)
        embed = discord.Embed(title="Hibajelentés!", description=f"```{message1}```", color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Hiba", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author} × Hiba", icon_url=self.client.user.avatar_url)
        await channel.send(embed=embed, content="@here")
        await ctx.reply("<:radon_pipa:811191514369753149> Sikeresen elküldtem a hibát!", mention_author=False)
    @commands.command()
    async def uptime(self, ctx):
        jelenlegi = time.time()
        uptime_raw = int(round(jelenlegi - start_ido))
        uptime = str(datetime.timedelta(seconds=uptime_raw))
        if 'day' in uptime:
        	uptime = uptime.replace('day', 'nap')
        embed = discord.Embed(description=f"{uptime} ideje vagyok elérhető!", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Futásidő", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author} × Uptime", icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)
    @commands.command(aliases=["pong", "connection", "net", "network"])
    @commands.cooldown(1, 3, type=commands.BucketType.user)
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.reply(content="Pingelés...", embed=None, mention_author=False)
        ping = round((time.monotonic() - before) * 1000)
        try:
            
            before2=time.monotonic()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM data")
            ping2raw = (time.monotonic() - before2)
            ping2 = str(ping2raw)[:6]
            cursor.fetchall()
            db.commit()
            embed = discord.Embed(description=f"Üzenetküldés ideje: `{ping}ms`\nBot pingje: `{round(self.client.latency * 1000)}ms`\nAdatbázis ping: `{ping2}ms`", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Pong! 🏓", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Ping", icon_url=self.client.user.avatar_url)
            await message.edit(content=None, embed=embed, mention_author=False)
        except:
            embed = discord.Embed(description=f"Üzenetküldés ideje: `{ping}`ms\nBot pingje: `{round(self.client.latency * 1000)}ms`\nAdatbázis ping: `Nem tudtam lekérni`", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Pong!", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Ping", icon_url=self.client.user.avatar_url)
            await message.edit(content=None, embed=embed, mention_author=False)

    @commands.command(usage=",aliases [parancs]", aliases=["alias", "al"])
    async def aliases(self, ctx, command):
        command = command.lower()
        try: command = self.client.get_command(command)
        except: await ctx.reply("Nem található ilyen parancs!", mention_author=False)
        aliases = command.aliases
        if aliases == None: 
            await ctx.reply("Ennek a parancsnak nincs aliasa!", mention_author=False)
            return
        a = ""
        for aliases in command.aliases:
            a = a + aliases + "\n"
        embed = discord.Embed(description=f"{command.name}\n{a}", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Alias", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Alias", icon_url=self.client.user.avatar_url)   
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",árfolyam [valuta]", aliases=["exchange", "exch", "ár", "arfolyam"])
    async def árfolyam(self, ctx, valasz):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15',"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        if valasz == "euro" or valasz == "euró":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=maF&sxsrf=ALeKk01GxrywcQOrodL7Fm-sLksgl64Shw%3A1602246229608&ei=VVaAX4PXJIKNrwT4j7_IBg&q=1+eur+to+huf&oq=1+eur&gs_lcp=CgZwc3ktYWIQARgAMgkIIxAnEEYQggIyBAgAEEMyBQgAELEDMgQIABBDMgUIABDLATIECAAQQzICCAAyAggAMgQIABBDMgUIABDLAToHCCMQ6gIQJzoECCMQJzoICAAQsQMQgwE6BQguELEDOgIILjoHCAAQsQMQQ1DxFFiXLmD9PGgCcAF4AIABhQGIAaAFkgEDMi40mAEAoAEBqgEHZ3dzLXdperABCsABAQ&sclient=psy-ab", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for euroget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                euro = euroget.get_text()
                await ctx.reply(f"Euró árfolyama: {euro} Forint", mention_author=False)
        elif valasz == "btc" or valasz == "bitcoin":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=vaF&sxsrf=ALeKk00wKOHMmYX9YbgjmG-NkeZRr9nCiw%3A1602246238253&ei=XlaAX-XwDpC53AOmqLSYDA&q=1+btc+to+huf&oq=1+btc+to+huf&gs_lcp=CgZwc3ktYWIQAzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJ1CEuwlY29YJYPzYCWgBcAF4AIABAIgBAJIBAJgBAKABAaoBB2d3cy13aXqwAQrAAQE&sclient=psy-ab&ved=0ahUKEwjll_6uwKfsAhWQHHcKHSYUDcMQ4dUDCAw&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Bitcoin árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "font":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=9xu&sxsrf=ALeKk009xKR-xdop5rncHbISYrvbiCIxEQ%3A1602246400840&ei=AFeAX8HoMumRrgST67roBg&q=1+font+to+huf&oq=1+font+to+huf&gs_lcp=CgZwc3ktYWIQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjICCAAyBggAEAcQHjIGCAAQBxAeMgYIABAHEB46BAgAEEc6BwgjELACECc6BAgAEA1QqIoIWMSTCGCllAhoAHACeACAAZ0BiAGBB5IBAzIuNpgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjB6MH8wKfsAhXpiIsKHZO1Dm0Q4dUDCAw&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Font árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "dollár":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=K0u&sxsrf=ALeKk00Bsb7nZx9atsV8v9nB6QZLGDy-pA%3A1602246535532&ei=h1eAX4zzH-qFrwSZ2JLYCQ&q=1+dollar+to+huf&oq=1+dollar+to+huf&gs_lcp=CgZwc3ktYWIQAzIJCCMQJxBGEIICMgYIABAHEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeOgwIIxCwAhAnEEYQggI6CAgAEAgQDRAeOgcIIxCwAhAnOggIABAIEAcQHlD1DVilFmD2F2gCcAB4AIABbogB0gGSAQMwLjKYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwjM0t68wafsAhXqwosKHRmsBJsQ4dUDCAw&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Dollár árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "frank":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?q=1+dfrank+to+huf&oq=1+dfrank+to+huf&aqs=chrome..69i57j0.5659j1j1&sourceid=chrome&ie=UTF-8", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Frank árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "jen":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01uFnBZQJJ0Ty25OzbnSdcD-Q0XdA%3A1602335304083&ei=SLKBX76qBO_2qwHElJ6ABg&q=1+jen+to+huf&oq=1+jen+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQCjoECAAQRzoFCAAQzQI6BggAEAcQHlCnkUxYkqVMYLiqTGgBcAF4AIABugGIAfUJkgEDMS45mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwi-7vCUjKrsAhVv-yoKHUSKB2AQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Jen árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "lej":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk00pxEYx683QkRL5LubbRDzC9kU54g%3A1602336556855&ei=LLeBX9vVM-THrgS83KzIDA&q=1+lej+to+huf&oq=1+lej+to+huf&gs_lcp=CgZwc3ktYWIQAzICCAA6BAgAEEc6CAgAEAcQChAeOgYIABAHEB5Qp8sKWOnUCmCP2gpoAHACeACAAXuIAfgEkgEDMS41mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjbm6DqkKrsAhXko4sKHTwuC8kQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Lej árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "zloty":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk03SGXdbVi35OECDeJA_J_SC8L21Dg%3A1602336735222&ei=37eBX9CHDafIrgTGnquYAw&q=1+zloty+to+huf&oq=1+zloty+to+huf&gs_lcp=CgZwc3ktYWIQAzICCAA6BAgAEEc6BggAEAcQHjoICAAQBxAKEB46BAgAEB46BAgAEA06CAgAEAgQDRAeUObXClii5Qpg4ucKaABwA3gAgAF2iAGJBpIBAzUuM5gBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwiQ86a_karsAhUnpIsKHUbPCjMQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Zloty árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "kuna":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk02Yz7o-BdwSvMPmapqMdRJsROG5pw%3A1602336914232&ei=kriBX8rRDdL3qwH-uJPYCA&q=1+kuna+to+huf&oq=1+kuna+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQQzoECAAQRzoHCCMQsAIQJzoECAAQDToICAAQCBANEB46AggAOgYIABAHEB5QzPQGWIqCB2CzhAdoAHACeACAAXaIAcIHkgEDMy42mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjK4tSUkqrsAhXS-yoKHX7cBIsQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Kuna árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "dinár":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01a9laB5ypw4GYi_5CtWct6DcLmjg%3A1602337030781&ei=BrmBX-KbL-LGrgTN6JnoBQ&q=1+din%C3%A1r+to+huf&oq=1+din%C3%A1r+to+huf&gs_lcp=CgZwc3ktYWIQAzICCAA6BAgAEEc6BwgjELECECc6BwgjELACECc6BggAEAcQHjoECAAQDToICAAQCBAHEB46BwgAEEYQggI6CAgAEAgQDRAeUMy8Cljtygpg6cwKaABwAngAgAGZAYgB9QeSAQMyLjeYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab&ved=0ahUKEwjitp7MkqrsAhVio4sKHU10Bl0Q4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Dinár árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "líra":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk020U2iY6SGaYzoWwgfGM5uwKgnsog%3A1602337325847&ei=LbqBX8OnM4rurgTK7am4Dw&q=1+l%C3%ADra+to+huf&oq=1+l%C3%ADra+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQIyBQgAEM0CMgUIABDNAjIFCAAQzQIyBQgAEM0COgQIABBHOgYIABAHEB46CAgAEAcQChAeOgQIABAeOgQIABANOggIABAIEA0QHlCd2gZYgegGYIbrBmgBcAJ4AIABb4gBuASSAQM0LjKYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab&ved=0ahUKEwiD8vfYk6rsAhUKt4sKHcp2CvcQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Líra árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "peso":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk03qdVi3NaIrSwZlAUtSIyoRRx9EKQ%3A1602337438793&ei=nrqBX-HzL8borgTA3bGICg&q=1+peso+to+huf&oq=1+peso+to+huf&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQCBAeOgQIABBHOgQIABANOggIABAIEA0QHjoFCAAQzQI6BggAEAcQHjoICAAQBxAKEB46CAgAEAgQBxAeUIGzB1ijxQdghMgHaABwA3gAgAF_iAHXBpIBAzMuNZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjhuuWOlKrsAhVGtIsKHcBuDKEQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Peso árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "hrivnya":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01Ykv6FWIMPrvFVmcklFq-3kVV1cA%3A1602337564119&ei=HLuBX43jBoeOrwTV26-ADQ&q=1+hvrinya+to+huf&oq=1+hvrinya+to+huf&gs_lcp=CgZwc3ktYWIQAzIJCAAQDRBGEIICOgQIABBHOgcIIxCwAhAnOgYIABAHEB46CAgAEAgQBxAeOgIIADoECAAQDVCO2AVYsO0FYKP6BWgAcAJ4AIABhgGIAYAJkgEDNC43mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwiN4cbKlKrsAhUHx4sKHdXtC9AQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Hrivnya árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "rúpia":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk03_H08c6tbuNpSXHabRn5kFt-b1EA%3A1602337731517&ei=w7uBX9r6HpKyrgSvpaLADQ&q=1+r%C3%BApia+to+huf&oq=1+r%C3%BApia+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQHjoECAAQRzoGCAAQDRAeOgYIABAHEB46BAgAEA1QjyRYjDRg0TVoAHACeACAAXeIAccGkgEDMy41mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwia6K-alarsAhUSmYsKHa-SCNgQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Rúpia árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "riál":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01eeRUthMDtd5cf5lRgA_XyLyRgpg%3A1602337740134&ei=zLuBX_fjB8T9rgTgqq9w&q=1+ri%C3%A1l+to+huf&oq=1+ri%C3%A1l+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQI6BAgAEEc6BwgjELACECc6BAgAEA06BggAEAcQHjoJCAAQDRBGEIICOggIABAIEAcQHlCyoARY3rAEYL22BGgBcAJ4AIABeYgBnQaSAQM1LjOYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab&ved=0ahUKEwj3-b2elarsAhXEvosKHWDVCw4Q4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Riál árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "rubel":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk014NZhiDGl3w7o-R-z50KxcaKrIIg%3A1602337814143&ei=FryBX-KgCM3orgS-972gDg&q=1+rubel+to+huf&oq=1+rubel+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQCjoECAAQRzoFCAAQzQI6BAgAEA06CAgAEAgQBxAeOgYIABAHEB46CQgAEA0QRhCCAjoHCAAQRhCCAjoICAAQBxAKEB5QsroEWN7IBGC7zARoAHACeACAAXaIAeEFkgEDMS42mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjig-PBlarsAhVNtIsKHb57D-QQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Rubel árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "sol":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk02VEjr_hmh7xLaHblNlVDEYyXx2Qw%3A1602337890576&ei=YryBX8HLIuz1qwGax7HwAg&q=1+sol+to+huf&oq=1+sol+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQIyBQgAEM0CMgUIABDNAjoECAAQRzoICAAQBxAKEB46AggAOgYIABAHEB46BAgAEA1Q3NICWKfmAmCE6QJoAHACeACAAWaIAewFkgEDNy4xmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjBhJzmlarsAhXs-ioKHZpjDC4Q4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Sol árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "afgán":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?q=1+afg%C3%A1n+to+huf&oq=1+afg%C3%A1n+to+huf&aqs=chrome..69i57j0i333l3.4468j0j7&sourceid=chrome&ie=UTF-8", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Afgán árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "kwanza":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk02xGhUfwFcVdHpD0RWI0OWEaKce9g%3A1603016418670&ei=4haMX6adKJ2GwPAP-aihwAs&q=1+kwanza+to+huf&oq=1+kwanza+to+huf&gs_lcp=CgZwc3ktYWIQAzoECAAQRzoFCAAQzQI6BAgAEA06CQgAEA0QRhCCAjoGCAAQBxAeOggIABAIEAcQHlCqkRtYor0bYKm-G2gBcAJ4AIABnQKIAb8LkgEFNS42LjGYAQCgAQGqAQdnd3Mtd2l6yAEFwAEB&sclient=psy-ab&ved=0ahUKEwimltDB9b3sAhUdAxAIHXlUCLgQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Kwanza árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "lek":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk00_xKUkqqvjlYkHOa0-175-la2zlw%3A1603031117569&ei=TVCMX4aiIvHIrgTjkrrgAg&q=1+leke+to+huf&oq=1+leke+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQI6BAgAEEc6BggAEAcQHjoICAAQBxAKEB46BAgjECdQgzBYgjVguzZoAHACeACAAWyIAf0DkgEDMS40mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjG_M2irL7sAhVxpIsKHWOJDiwQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Lek árfolyama: {btc} Forint", mention_author=False)
        else: await ctx.reply("Nincs ilyen választási lehetőség! Választási lehetőségek: dollár, euró, bitcoin, font, frank, jen, lej, zloty, kuna, dinár, líra, peso, hrivnya, rúpia, riál, rubel, kwanza, lek afgán vagy sol.", mention_author=False)

    @commands.command(usage=",youtube [videó cím]", aliases=["youtube", "ytkeresés", "ytsearch"])
    async def yt(self, ctx, *, search):
        import re
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        link = 'http://www.youtube.com/watch?v=' + search_results[0]
        embed = discord.Embed( description=f"A legelső találat a következő. Link: {link}", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="YouTube keresés", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × YouTube", icon_url=self.client.user.avatar_url)  
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",időjárás [város]", aliases=["weather", "idojaras"])
    async def időjárás(self, ctx, *, city: str):
        xd = await ctx.reply("Kérlek várj...", mention_author=False)
        import requests
        city_name = city
        complete_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b80b0690ff11eef06278e0f611c01e09"
        response = requests.get(complete_url)
        x = response.json()
        channel = ctx.message.channel
        if x["cod"] != "404":
            async with channel.typing():
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                #wrapper
                if weather_description == "shower rain": a = "Záporeső"
                elif weather_description == "broken clouds": a = "Felszakadozott felhőzet"
                elif weather_description == "haze": a = "Köd"
                elif weather_description == "few clouds": a = "Kevés felhő"
                elif weather_description == "mist": a = "Köd"
                elif weather_description == "clear sky": a = "Tiszta ég"
                elif weather_description == "cattered clouds": a = "Szétszórt felhőzet"
                elif weather_description == "fog": a="Köd"
                elif weather_description == "rain": a = "Eső"
                elif weather_description == "thunderstorm": a = "Vihar"
                elif weather_description == "snow": a = "Hó"
                elif weather_description == "light rain": a = "Eső"
                elif weather_description == "overcast clouds": a = "Borult felhők"
                else:
                    embed = discord.Embed(description="Nem tudtam lekérni az időjárást! Kérlek próbáld meg később!<:radon_x:856423841667743804> ", color=0xff0000, timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)
                embed = discord.Embed(title="Időjárás", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="Leírás", value=f"**{a}**", inline=False)
                embed.add_field(name="Fok(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
                embed.add_field(name="Páratartalom(%)", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(name="Légköri Nyomás(hPa)", value=f"**{current_pressure}hPa**", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embed.set_author(name="Időjárás: {}".format(city_name), icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f"{ctx.author.name} × Időjárás", icon_url=self.client.user.avatar_url) 
                await xd.edit(embed=embed)
        else:
            embed = discord.Embed(description="Nem található város, vagy nincs adat erről a városról! <:radon_x:856423841667743804> ", color=0xff0000, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Hiba", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",say [üzenet]")
    async def say(self, ctx, *, message):
        if ctx.author.guild_permissions.manage_messages:
            if not ctx.message.author.bot:
                if "@" in message: return
                await ctx.send(message)
                await ctx.message.delete()
            else:
                pass
            
        else:
            perm = "Üzenetek kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",embedsay [üzenet]", aliases=["esay","embeds", "embed", "sayembed"])
    async def embedsay(self, ctx, *,message1):
        if not ctx.message.author.bot:
            await ctx.message.delete()
            embed = discord.Embed(description=message1, color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"{ctx.author.name} × Embedsay", icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(usage=",coloresay [HEX színkód] [üzenet]", aliases=["ce","colorembeds", "colorembed", "saycolorembed", "colore", "cembed", "colorembedsay"])
    async def coloresay(self, ctx, color1, *, message):
        if not ctx.message.author.bot:
            await ctx.message.delete()
            embed = discord.Embed(description=message, color=color1, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"{ctx.author.name} × Embedsay", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)



    @commands.command(aliases=["server", "servers", "szerver", "szerverszám"])
    async def szerverek(self, ctx):
        servers = len(self.client.guilds)
        embed = discord.Embed(description=f"A bot jelenleg {servers} szerveren elérhető!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Szerverek", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Szerverek", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",szavazás [üzenet]", aliases=["szavazas", "vote", "poll"])
    async def szavazás(self, ctx, *, msg):
        await ctx.message.delete()
        embed = discord.Embed(description=msg, color = 0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Szavazás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Szavazás", icon_url=self.client.user.avatar_url)
        message = await ctx.send(embed=embed)
        await message.add_reaction('<:radon_check:856423841612824607>')
        await message.add_reaction('<:radon_x:856423841667743804>')

    @commands.command(aliases=["meghív", "inv"])
    async def invite(self, ctx):
        embed = discord.Embed(description="A bot meghívásához [**kattints ide!**](https://discord.com/oauth2/authorize?client_id=713014602891264051&permissions=8&scope=bot%20applications.commands)", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Meghívás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Meghívás", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["dc", "dev"])
    async def support(self, ctx):
        embed = discord.Embed(description="A support szerverre való belépéshez [**kattints ide!**](https://dc.radonbot.hu)", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Support szerver", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Support", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",kérdés [kérdésed]", aliases=["kerdes", "question", "8ball"])
    async def kérdés(self, ctx, *,message1):
        kérdés = ['Igen', 'Nem', 'Nem tudom', 'Biztosan', 'Kérdezz valaki mást...', 'Esélyes', 'Esélytelen', 'Nem valószínű']
        embed = discord.Embed(color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="8ball", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Kérdés", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Kérdés", value=message1)
        embed.add_field(name="Válasz", value=random.choice(kérdés))
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["ui","useri","uinfo", "uf", "ufind", "usersearch", "us", "usearch"], usage=",userinfo [felhasználó]")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        embed = discord.Embed(title="Felhasználó információi", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name="Infók", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Infók", icon_url=self.client.user.avatar_url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Beceneve", value=member.display_name)
        embed.add_field(name="Név", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Fiókját létrehozta", value=str(member.created_at).replace("-", ". "))
        embed.add_field(name="A szerverre belépett", value=str(member.joined_at).replace("-", ". "))
        embed.add_field(name="Legmagasabb rangja", value=member.top_role.mention)
        if str(member.status).title(): embed.add_field(name="Státusza", value=str(member.status).title())
        try: embed.add_field(name="Aktivitása", value=f"{str(member.activity.type).split('.')[-1].title()}: {member.activity.name}")
        except: embed.add_field(name="Aktivitása", value=f"Nincs megadva")
        a = "Igen" if member.bot else "Nem"
        embed.add_field(name="Bot?", value=a)
        embed.add_field(name=f"Összes rangja ({len(roles)})", value=", ".join([role.mention for role in roles]), inline=False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["si","serveri","sinfo", "szerverinfó", "szerverinfo", "szi"])
    async def serverinfo(self, ctx):
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
        len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
        len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
        len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
        embed = discord.Embed(title=f"Szerver Információ - {ctx.author.guild.name}", color=0xFF9900, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=ctx.author.guild.icon_url)
        embed.set_author(name="Szerverinfók", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Szerverinfók", icon_url=self.client.user.avatar_url)
        embed.add_field(name="ID", value=ctx.guild.id)
        embed.add_field(name="Tulajdonos", value=ctx.guild.owner)
        embed.add_field(name="Nitro boostok száma", value = f"{ctx.guild.premium_subscription_count}", inline = True)
        embed.add_field(name="Nitro boost szintje", value = f"{ctx.guild.premium_tier}", inline = True)
        embed.add_field(name="Régió", value=ctx.guild.region)
        embed.add_field(name="Szerver létrejött", value=ctx.guild.created_at.strftime("%Y. %m. %d. %H:%M:%S"))
        embed.add_field(name="Tagok", value=len(ctx.guild.members))
        embed.add_field(name="Emberek", value=len(list(filter(lambda m: not m.bot, ctx.guild.members))))
        embed.add_field(name="Botok", value=len(list(filter(lambda m: m.bot, ctx.guild.members))))
        embed.add_field(name="Kitiltott tagok", value=len(await ctx.guild.bans()))
        embed.add_field(name="Szöveges csatornák", value=len(ctx.guild.text_channels))
        embed.add_field(name="Hang csatornák", value=len(ctx.guild.voice_channels))
        embed.add_field(name="Kategóriák", value=len(ctx.guild.categories))
        embed.add_field(name="Rangok", value=len(ctx.guild.roles))
        embed.add_field(name="Meghívások", value=len(await ctx.guild.invites()))
        embed.add_field(name = "AFK csatorna", value = f"{ctx.guild.afk_channel}", inline = True)
        embed.add_field(name = "AFK időtartam", value = f"{ctx.guild.afk_timeout / 60} perc", inline = True)
        embed.add_field(name="Státuszok", value= f"{statuses[0]} 🟢 {statuses[1]} 🟡 {statuses[2]} 🔴 {statuses[3]} ⚪")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["névnap", "nday", "nameday"])
    async def nevnap(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://anevnap.hu", headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15', "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}) as f:
                import bs4
                r = await f.read()
            soup = bs4.BeautifulSoup(r, features="html.parser")
            for a in soup.find_all('span', {'class': 'nevnapkiemel'}):
                asd = a.get_text()
                await ctx.reply(f"A mai névnap: {asd}", mention_author=False)

    @commands.command(aliases=["yukishiro"])
    async def yuki(self, ctx):
        await ctx.reply("Szeret fejlesztgetni és persze szeret programozni.")

    @commands.command(usage=",roleinfo [rang]")
    async def roleinfo(self, ctx, role):
        role = await commands.RoleConverter().convert(ctx, role)

        embed = discord.Embed( color=0xFF9900, timestamp=ctx.message.created_at)
        embed.set_author(name="Rang információk", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Roleinfo", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Rang neve", value=role.name, inline = False)
        embed.add_field(name="Rang ID-ja", value=role.id, inline = False)
        embed.add_field(name="Rang poziciója", value=f"{role.position}/{len(ctx.guild.roles)}", inline = False)
        embed.add_field(name="Rang hány emberen van", value=len(role.members), inline = False)
        embed.add_field(name="Létrehozva ekkor", value=role.created_at.strftime("%Y. %m. %d. %H:%M:%S"), inline = False)
        embed.add_field(name="Színe", value=role.color, inline = False)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",userfind [ID vagy név#tag]")
    async def userfind(self, ctx, usr):
        brk = False
        if not str(usr).isdigit():
            for x in self.client.guilds:
                if brk:
                    break
                for k in x.members:
                    if str(k) == usr:
                        embed = discord.Embed( color=0xFF9900, timestamp=ctx.message.created_at)
                        embed.set_author(name="Felhasználó kereső", icon_url=ctx.author.avatar_url)
                        embed.set_footer(text=f"{ctx.author.name} × Userfind", icon_url=self.client.user.avatar_url)
                        embed.set_thumbnail(url=k.avatar_url)
                        embed.add_field(name="Felhasználó neve", value=str(k), inline = False)
                        embed.add_field(name="Felhasználó ID-ja", value=k.id, inline = False)
                        embed.add_field(name="Felhasználó létrehozva ekkor", value=k.created_at.strftime("%Y. %m. %d. %H:%M:%S"), inline = False)
                        embed.add_field(name="Bot?", value="Igen" if k.bot else "Nem", inline = False)
                        embed.add_field(name="Profilképe", value=f"[Katt ide]({k.avatar_url})")
                        await ctx.reply(embed=embed, mention_author=False)
                        brk = True
                        break
        else:
            print("id")
            k = self.client.get_user(int(usr))
            embed = discord.Embed( color=0xFF9900, timestamp=ctx.message.created_at)
            embed.set_author(name="Felhasználó kereső", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Userfind", icon_url=self.client.user.avatar_url)
            embed.set_thumbnail(url=k.avatar_url)
            embed.add_field(name="Felhasználó neve és tagje", value=str(k), inline = False)
            embed.add_field(name="Felhasználó ID-ja", value=k.id, inline = False)
            embed.add_field(name="Felhasználó létrehozva ekkor", value=k.created_at.strftime("%Y. %m. %d. %H:%M:%S"), inline = False)
            embed.add_field(name="Bot?", value="Igen" if k.bot else "Nem", inline = False)
            embed.add_field(name="Profilképe", value=f"[Katt ide]({k.avatar_url})", inline = False)
            embed.add_field(name="Említés", value=k.mention, inline = False)
            await ctx.reply(embed=embed, mention_author=False)

 
        

def setup(client):
    client.add_cog(Basic(client))

import asyncio
import discord
from discord.ext import commands
import json
import datetime
time_window_milliseconds = 1500
max_msg_per_window = 5
author_msg_times = {}
owners = [609764483229024297, 648168353453572117, 654721418273226793, 406137394228625419]
import discordwebhook

rulesmsg = """❗Obszcén, trágár kifejezések használata tilos!
❗Mások szidalmazása tilos!
❗Tilos bármiféle felnőtt tartalom megosztása!
❗Tilos bármilyen kártékony fájlokat, kódokat megosztani!
❗Tilos személyes információkat kiadni (Lakcím, teljes név, stb.)
❗A rendszert túlterhelni (spam, stb.) tilos!
❗Üres üzenetek(`** **`, stb) küldése tilos!
❗Hírdetni tilos!


❗**A szabályzat megszegése kitiltással járhat a GlobalChatből**
❗**A szabályzat az összes GlobalChat csatornára vonatkozik!**
❗**A szabályzat nem ismerete nem mentesít!**


Módosítva: 2021. 05. 10.

Szabályzat bárhol elérhető: `,gcrules`
A változás jogát fenntartjuk!"""

async def send1(message, webhooks):
    for webhook in webhooks:
        try:
            avatar = str(message.author.avatar_url_as(format="png", size=1024)).replace("?size=1024", "")
            xd = discordwebhook.Discord(url=webhook)
            if message.author.id in owners:
                await xd.post(
                    username=f"T » {message.author.name}ㆍ{message.guild.name}",
                    content=message.content,
                    avatar_url=avatar
                )
            else:
                await xd.post(
                    username=f"{message.author.name}ㆍ{message.guild.name}",
                    content=message.content,
                    avatar_url=avatar
                )
            await asyncio.sleep(0.5)
            
            continue
        except: continue

async def send2(message, webhooks):
    for webhook in webhooks:
        try:
            avatar = str(message.author.avatar_url_as(format="png", size=1024)).replace("?size=1024", "")
            xd = discordwebhook.Discord(url=webhook)
            if message.author.id in owners:
                await xd.post(
                    username=f"T » {message.author.name}ㆍ{message.guild.name}",
                    content=message.content,
                    avatar_url=avatar
                )
            else:
                await xd.post(
                    username=f"{message.author.name}ㆍ{message.guild.name}",
                    content=message.content,
                    avatar_url=avatar
                )
            await asyncio.sleep(0.5)
            continue
        except: continue

async def send3(message, webhooks):
    for webhook in webhooks:
        try:
            avatar = str(message.author.avatar_url_as(format="png", size=1024)).replace("?size=1024", "")
            xd = discordwebhook.Discord(url=webhook)
            if message.author.id in owners:
                await xd.post(
                    username=f"T » {message.author.name}ㆍ{message.guild.name}",
                    content=message.content,
                    avatar_url=avatar
                )
            else:
                await xd.post(
                    username=f"{message.author.name}ㆍ{message.guild.name}",
                    content=message.content,
                    avatar_url=avatar
                )
            await asyncio.sleep(0.5)
            continue
        except: continue

async def send1_pic(message, url, webhooks):
    for webhook in webhooks:
        try:
            avatar = str(message.author.avatar_url_as(format="png", size=1024)).replace("?size=1024", "")
            xd = discordwebhook.Discord(url=webhook)
            if message.author.id in owners:
                await xd.post(
                    username=f"T » {message.author.name}ㆍ{message.guild.name}",
                    content=f"{message.content}\n\n*{message.author.name} fájlt csatolt:* {url}",
                    avatar_url=avatar
                )
                
                continue
            else:
                await xd.post(
                    username=f"{message.author.name}ㆍ{message.guild.name}",
                    content=f"{message.content}\n\n*{message.author.name} fájlt csatolt:* {url}",
                    avatar_url=avatar
                )
            continue
        except: 
            continue

async def send2_pic(message, url, webhooks):
    for webhook in webhooks:
        try:
            avatar = str(message.author.avatar_url_as(format="png", size=1024)).replace("?size=1024", "")
            xd = discordwebhook.Discord(url=webhook)
            if message.author.id in owners:
                await xd.post(
                    username=f"T » {message.author.name}ㆍ{message.guild.name}",
                    content=f"{message.content}\n\n*{message.author.name} fájlt csatolt:* {url}",
                    avatar_url=avatar
                )
                continue
            else:
                await xd.post(
                    username=f"{message.author.name}ㆍ{message.guild.name}",
                    content=f"{message.content}\n\n*{message.author.name} fájlt csatolt:* {url}",
                    avatar_url=avatar
                )
            continue
        except: 
            continue

async def send3_pic(message, url, webhooks):
    for webhook in webhooks:
        try:
            avatar = str(message.author.avatar_url_as(format="png", size=1024)).replace("?size=1024", "")
            xd = discordwebhook.Discord(url=webhook)
            if message.author.id in owners:
                await xd.post(
                    username=f"T » {message.author.name}ㆍ{message.guild.name}",
                    content=f"{message.content}\n\n*{message.author.name} fájlt csatolt:* {url}",
                    avatar_url=avatar
                )
                continue
            else:
                await xd.post(
                    username=f"{message.author.name}ㆍ{message.guild.name}",
                    content=f"{message.content}\n\n*{message.author.name} fájlt csatolt:* {url}",
                    avatar_url=avatar
                )
            continue
        except: 
            continue


swears = ["anyád", "kurva", "retek", "rák", "tetű", "tetves", "dögölj meg", "halj meg", "cigány", "román", "pénisz", "fasz", "pina", "vagina", "f4sz", "p1na", "nigga", "nigger", "niga", "niger", "geci", "köcsög", "g3ci", "buzi"]

class GlobalChat(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=",setglobalchat [#csatorna]", aliases=["setgchat"])
    async def setglobalchat(self, ctx, channel):
        if ctx.author.guild_permissions.administrator:
            try: channel = await commands.TextChannelConverter().convert(ctx, channel)
            except: await ctx.send("Nem található ilyen csatorna!")
            webhook = await channel.create_webhook(name="Radon GlobalChat")
            with open("numberGc.json", "r") as f:
                numDB = json.load(f)
                id = numDB["number"]
            with open("gcreq.json", "r") as f:
                db = json.load(f)
                db[str(id)] = {}
                db[str(id)]["webhook"] = str(webhook.url)
                db[str(id)]["channel_id"] = str(channel.id)
                db[str(id)]["guild_id"] = str(ctx.guild.id)
                with open("gcreq.json", "w") as f:
                    json.dump(db, f, indent=4)
            numDB["number"] = id + 1
            with open("numberGc.json", "w") as f:
                json.dump(numDB, f, indent=4)
            adminchannel = self.client.get_channel(856493897392193576)
            embed = discord.Embed(title=f"Kérelem × {str(ctx.author)}", timestamp=datetime.datetime.utcnow(), color=ctx.author.color)
            embed.add_field(name="Szerver", value=ctx.guild.name)
            embed.add_field(name="Tagok", value=len(ctx.guild.members))
            embed.add_field(name="Csatorna", value=channel.name)
            embed.add_field(name="ID", value=id)
            embed.set_footer(text=f"Elfogadáshoz: ,gcaccept {id}")    
            await adminchannel.send(embed=embed)
            await ctx.send("Kérelmed sikeresen elküldve!") 
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)

    @commands.command(aliases=["gcheck"])
    async def gccheck(self, ctx):
        with open("gc.json", "r") as f:
            asd = json.load(f)
            await ctx.send(f"A globalchat {len(asd['hooks'])} szerveren van bekapcsolva.")

    @commands.command(usage=[",gcaccept [ID]"])
    async def gcaccept(self, ctx, id: str):
        if ctx.channel.id == 856493897392193576:
            a = []
            b = []
            try:
                with open("gcreq.json", "r") as f:
                    dbQ = json.load(f)
                with open("gc.json", "r") as f:
                    db = json.load(f)
                    webhook = dbQ[str(id)]["webhook"]
                    for x in db["hooks"]:
                        xdxd = str(x).replace("['", "").replace("']", "")
                        a.append(xdxd)
                    a.append(webhook)
                    db["hooks"] = a
                    for p in db["channels"]:
                        xdx = str(p).replace("['", "").replace("']", "")
                        b.append(xdx)
                    b.append(dbQ[str(id)]["channel_id"])
                    db["channels"] = b
                    guild = self.client.get_guild(int(dbQ[str(id)]["guild_id"]))
                    channel = self.client.get_channel(int(dbQ[str(id)]["channel_id"]))
                await ctx.send("Elfogadva!")
                with open("gc.json", "w") as f:
                    json.dump(db, f, indent=4)
                with open("gcreq.json", "w") as f:
                    json.dump(dbQ, f, indent=4)
            except:
                await ctx.send("Nem található ilyen ID!")
                raise
            for channelk in db["channels"]:
                try:
                    x = self.client.get_channel(int(channelk))
                    await x.edit(topic=f"Írj ebbe a csatornába ha szeretnél másik szerverekkel csevegni! Jelenleg **{len(db['hooks']) + len(db['hooks1']) + len(db['hooks2'])}** szerverre lesz elküldve az üzenet!")
                    await asyncio.sleep(2)
                    continue
                except:
                    continue
            await guild.owner.send(f"A GlobalChat kérelmed el lett fogadva a {guild.name} szerveren, a GlobalChat üzenetei mostantól a {channel.name}-ba/be fognak jönni.")
        else:
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return 

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            with open("banneds.json", "r") as f:
                banned_members = json.load(f)["members"]
            if int(message.author.id) in banned_members:
                return
            with open("gc.json", "r") as f:
                asd = json.load(f)
                channels = asd["channels"]
                webhooks = asd["hooks"]
                webhooks1 = asd["hooks1"]
                webhooks2 = asd["hooks2"]


            if str(message.channel.id) in str(channels):
                if "discord" in message.author.name:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"{message.author} hírdetni próbált\n\nInnen: {message.guild.name}")
                    return
                if "xhamster.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "xnxx.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "youtube.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "youtu.be" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "xvideos.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "@" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) pingelni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "discord.gg" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "discord.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "discord.io" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "dsc.lol" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "pornhub.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "ad.fly" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "bit.ly" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "grabify.link" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) IP grabbelni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "top.gg" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "disboard" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "disforge" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "discordservers.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "discordbee.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "discords.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                if "discordexpert.com" in message.content:
                    channel = self.client.get_channel(856493897392193576)
                    await channel.send(f"**{message.author}** (`{message.author.id}`) hírdetni próbált\n\nInnen: {message.guild.name}\n\n||{message.content}||")
                    return
                
                if message.content.startswith(","): return
                with open("gclog.txt", "a") as f:
                        f.writelines(f"\n{message.guild.name} ({message.guild.id}): {str(message.author)} ({message.author.id}): {message.content}")
                        f.close()
                if message.attachments:
                    await message.delete()
                    url = message.attachments[0].url
                    await send1_pic(message=message, url=url, webhooks=webhooks)
                    
                    await send2_pic(message=message, url=url, webhooks=webhooks1)
                    await send3_pic(message=message, url=url, webhooks=webhooks2)
                else:
                        
                    await message.delete()
                    await send1(message=message, webhooks=webhooks)
                    await send2(message=message, webhooks=webhooks1)
                    await send3(message=message, webhooks=webhooks2)
                        


    @commands.command(usage=",gcban [add/remove] [ID] [indok]")
    async def gcban(self, ctx, method, xd: int):
        if ctx.channel.id == 856493897392193576:
            if method == "add":
                a = []
                try:
                    with open("banneds.json", "r") as f:
                        db = json.load(f)
                        for x in db["members"]:
                            a.append(x)
                        a.append(xd)
                        db["members"] = a
                    with open("banneds.json", "w") as f:
                        json.dump(db, f, indent=4)
                    await ctx.reply("Kitiltva")
                except: return

            elif method == "remove":
                a = []
                with open("banneds.json", "r") as f:
                        db = json.load(f)
                        for x in db["members"]:
                            a.append(x)
                        a.remove(xd)
                        db["members"] = a
                with open("banneds.json", "w") as f:
                        json.dump(db, f, indent=4)
                await ctx.reply("Törölve")
            else: await ctx.send("Nincs ilyen opció")



    @commands.command(usage=",gcdeny [ID] [indok]", aliases=["gcdecline"])
    async def gcdeny(self, ctx, id: int, *, reason):
        if ctx.channel.id == 856493897392193576:
            with open("gcreq.json", "r") as f:
                db = json.load(f)
                guild = db[int(id)]["guild_id"]
            with open("gcreq.json", "w") as f:
                json.dump(db, f, indent=4)
                await guild.owner.send(f"GlobalChat kérelmed elutasítva! Indok: {reason}")
                await ctx.send("Elutasítva! :sunglasses:")
        else:
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.command()
    async def gcfix(self, ctx):
        with open("gc.json", "r") as f:
            db = json.load(f)
            for channel in db["channels"]:
                x = self.client.get_channel(int(channel))
                if x == None: 
                    continue
                else:
                    await x.edit(topic=f"Írj ebbe a csatornába ha szeretnél másik szerverekkel csevegni! Jelenleg *{len(db['hooks']) + len(db['hooks1']) + len(db['hooks2'])}** szerverre lesz elküldve az üzenet!")
                    await asyncio.sleep(2)
            await ctx.send("kesz")

    @commands.command()
    async def gcrules(self, ctx):
        embed = discord.Embed(title="🌎 GlobalChat szabályzat", description=rulesmsg, timestamp=datetime.datetime.utcnow(), color=ctx.author.color)
        await ctx.send(embed=embed)

    """@commands.command()
    async def blacklist(ctx, type, id: int, *, reason):
        if type == "add":
            blacklisted.append(id)
            await ctx.send(f"**{id}** sikeresen felkerült a listára!")
        if type == "rem" or "remove":
            pass"""
def setup(client):
    client.add_cog(GlobalChat(client))

import discord
from discord.ext import commands
import datetime
from discord.utils import get
from google_speech import Speech
import asyncio
import aiohttp
import random
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class Update(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=",rules [szabály1|szabály2|szabály3|...]")
    async def rules(self, ctx):
        try:
            await ctx.reply("A szabályokat újabb üzenetek beküldésével választhatod el. Max 15, minimum 5 szabály..")
            def check(m): return m.author == ctx.author and m.channel == ctx.channel
            kerdesek = ["Melyik csatornába küldjem az üzenetet?", "Mi az 1. szabály?", "Mi a 2. szabály?", "Mi a 3. szabály?", "Mi a 4. szabály?", "Mi az 5. szabály?", "Mi a 6. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 7. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 8. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 9. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 10. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 11. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 12. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 13. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 14. szabály? (Ha nincs, írd be: `nincs`)", "Mi a 15. szabály? (Ha nincs, írd be: `nincs`)", "Milyen szöveg legyen a szabályok előtt? (Emojit csak akkor fogad el, ha bent van azon a szerveren, ahol az emoji van.)", "Legyen rajta everyone ping? (`y/n`)"]
            valaszok = []
            for i in kerdesek:
                await ctx.send(i)
                try: msg = await self.client.wait_for('message', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Nem válaszoltál időben, a szabályzat készítő bezárul.')
                    return
                else:
                    if ctx.message.content == "nincs" or ctx.message.content == "none" and kerdesek[6] or kerdesek[7] or kerdesek[8] or kerdesek[9] or kerdesek[10] or kerdesek[11] or kerdesek[12] or kerdesek[13] or kerdesek[14] or kerdesek[15]:
                        pass
                    valaszok.append(msg.content)
            try:
                channel_id = int(valaszok[0][2:-1])
            except:
                await ctx.send(f"Hibás csatornaformátum! Használj {ctx.channel.mention}-t!")
                return
            channel = self.client.get_channel(channel_id)
            szabaly1 = valaszok[2]
            szabaly2 = valaszok[3]
            szabaly3 = valaszok[4]
            szabaly4 = valaszok[5]
            szabaly5 = valaszok[6]
            szabaly6 = valaszok[7]
            szabaly7 = valaszok[8]
            szabaly8 = valaszok[9]
            szabaly9 = valaszok[10]
            szabaly10 = valaszok[11]
            szabaly11 = valaszok[12]
            szabaly12 = valaszok[13]
            szabaly13 = valaszok[14]
            szabaly14 = valaszok[15]
            szabaly15 = valaszok[16]
            vegen = valaszok[17]
            vanping = valaszok[18]
            if szabaly1:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly6:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly7:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly8:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly9:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n{vegen} **9:** {szabaly9}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly10:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n{vegen} **9:** {szabaly9}\n{vegen} **10:** {szabaly9}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly11:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n{vegen} **9:** {szabaly9}\n{vegen} **10:** {szabaly11}\n{vegen} **11:** {szabaly11}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly12:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n{vegen} **9:** {szabaly9}\n{vegen} **10:** {szabaly11}\n{vegen} **11:** {szabaly11}\n{vegen} **12:** {szabaly12}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly13:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n{vegen} **9:** {szabaly9}\n{vegen} **10:** {szabaly11}\n{vegen} **11:** {szabaly11}\n{vegen} **12:** {szabaly12}\n{vegen} **13:** {szabaly13}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly14:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n{vegen} **9:** {szabaly9}\n{vegen} **10:** {szabaly11}\n{vegen} **11:** {szabaly11}\n{vegen} **12:** {szabaly12}\n{vegen} **13:** {szabaly13}\n{vegen} **14:** {szabaly14}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            elif szabaly15:
                embed = discord.Embed(title="Szabályzat", description=f"{vegen} **1:** {szabaly1}\n{vegen} **2:** {szabaly2}\n{vegen} **3:** {szabaly3}\n{vegen} **4:** {szabaly4}\n{vegen} **5:** {szabaly5}\n{vegen} **6:** {szabaly6}\n{vegen} **7:** {szabaly7}\n{vegen} **8:** {szabaly8}\n{vegen} **9:** {szabaly9}\n{vegen} **10:** {szabaly11}\n{vegen} **11:** {szabaly11}\n{vegen} **12:** {szabaly12}\n{vegen} **13:** {szabaly13}\n{vegen} **14:** {szabaly14}\n{vegen} **15:** {szabaly15}\n\nEmellett tartsd be a Discord (ÁSZF-jét)[https://dis.gd/tos) és a (Közösségi Irányelveket)[https://dis.gd/guidelines]", timestamp=datetime.datetime.utcnow(), color=discord.Color.green())
            else:
                pass
            if vanping in ("y", "yes", "be", "igen"):
                await channel.send(content="@everyone", embed=embed)
            elif vanping in ("n", "no", "ki", "nem"):
                await channel.send(embed=embed)
            else:
                await ctx.send("Nem jó formátum! (Ping)")
        except:
            raise

    @commands.command(usage=",voicesay <üzenet>")
    async def voicesay(self, ctx, *, text):
        try:
            lang = "hu"
            speech = Speech(text, lang)
            print("[VOICESAY] ~> Csatlakozás folyamatban...")
            voicechannel = ctx.message.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                if not ctx.author.voice.channel == ctx.voice_client.channel:
                    print("[VOICESAY] ~> A bot másik hangcsatornában van")
                    embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xFF0000)
                    get(self.client.voice_clients, guild=ctx.guild).play(discord.FFmpegPCMAudio(speech.play(), **FFMPEG_OPTIONS))
                    await ctx.send(embed=embed)
                    return
                else:
                    print("[VOICESAY] ~> Letöltés megkezdése...")
                    #ydl_opts = {'format': 'bestaudio', 'track': 'title'}
                    print("[VOICESAY] ~> Zene elindítva")
            else:
                await voicechannel.connect()
            await ctx.guild.change_voice_state(channel=voicechannel, self_mute=False, self_deaf=True)
        except AttributeError:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Nem vagy hangcsatornában!", color=0xFF0000)
                await ctx.send(embed=embed)
        except commands.errors.CommandInvokeError:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Ismeretlen hiba történt", color=0xFF0000)
                await ctx.send(embed=embed)

    @commands.command(aliases=["koalák", "koalak", "koalas", "koalapic", "koalakep"])
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/img/koala') as r:
                if r.status == 200:
                    js = await r.json()
                embed = discord.Embed(color=0xFF9900, title="🐨 Koalák")
                embed.set_image(url=js["link"])
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["goats", "kecske", "kecskék", "pi", "pí"])
    async def goat(self, ctx):
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://www.reddit.com/r/goats/new.json?sort=hot') as r:
                        res = await r.json()
                        embed = discord.Embed(color=0xFF9900, title="🐐 Kecskék")
                        embed.set_image(url=res['data']['children'][random.randint(0, 10)]['data']['url'])
                        await ctx.reply(embed=embed, mention_author=False)
        except:
            raise
        

def setup(client):
    client.add_cog(Update(client))

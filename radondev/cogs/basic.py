import discord
from discord.ext import commands, tasks
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
import psutil
dateT = datetime.datetime.utcnow()
import discord_webhook

class Basic(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_delete(self, ctx):
        cleanmsg = ctx.content
        async for entry in ctx.guild.audit_logs(limit=1, action=discord.AuditLogAction.message_delete):
            if entry.target != ctx.author:
                embed = discord.Embed(title="Üzenet törlése", description=f"{ctx.author.mention} (**{ctx.author}**) törölte a saját üzenetét a {ctx.channel.mention} csatornában.", color=0xFF9900)
                embed.add_field(name="Üzenet", value=cleanmsg, inline=False)
                channel = self.client.get_channel(855526480267313212)
                await channel.send(embed=embed)
            else:
                embed = discord.Embed(title="Üzenet törlése", description=f"{ctx.author.mention} (**{ctx.author}**) üzenetét törölték a {ctx.channel.mention} csatornában.", color=0xFF9900)
                embed.add_field(name="Üzenet", value=cleanmsg, inline=False)
                embed.add_field(name="Törölte", value=f"{entry.user.mention} (**{entry.user}**)")
                channel = self.client.get_channel(855526480267313212)
                await channel.send(embed=embed)

    @commands.command(usage=",edit [csatorna] [üzenet ID] [új üzenet]")
    async def edit(self, ctx, channel: discord.TextChannel, msgid: int, *, content):
        xd = await ctx.send("Üzenet keresése...")
        msg = await channel.fetch_message(msgid)
        if msg.author.id != 838835305342566440:
            await xd.edit("Az üzenet nem az enyém, ezért nem tudom szerkeszteni!")
            await asyncio.sleep(5)
            await xd.delete()
        await msg.edit(content=content)
        await xd.edit("Üzenet szerkesztve!")
        await ctx.message.delete()
        await asyncio.sleep(5)
        await xd.delete()

    @commands.command()
    async def embedbuilder(self, ctx):
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
            embed=discord.Embed(title=valaszok[1], description=valaszok[2], timestamp=datetime.datetime.utcnow() if timestamp else None, color=0xff9900)
            if author and aicon: embed.set_author(name=valaszok[3], icon_url=valaszok[5])
            if footer and ficon: embed.set_footer(text=valaszok[4], icon_url=valaszok[6])
            if author and not aicon: embed.set_author(name=valaszok[3])
            if footer and not ficon: embed.set_footer(text=valaszok[4])
            await channel.send(embed=embed)
        except:
            raise

    @commands.command()
    async def cuccxd(self, ctx, *, cucc):
        await ctx.send(cucc)

    @commands.command(aliases=["fekudj", "feküdj"])
    async def fekszik(self, ctx, member: discord.Member):
        if member == ctx.author:
            await ctx.reply("Magadat akarod elküldeni aludni? :(", mention_author=False)
            return
        embed = discord.Embed(title="Fekszik", description=f"{ctx.author.mention} elküldte {member.mention} felhasználót aludni!", color=0xFF9900, timestamp=datetime.datetime.utcnow(), footer=f"{ctx.author} × Radon")
        await ctx.send(embed=embed)

    @commands.command(aliases=["derike", "vg"])
    async def vgsgamersawards(self, ctx):
        embed = discord.Embed(title="VG's GamersAwards")
        embed.add_field(name="Discord szerver", value="Hamarosan...")
        embed.add_field(name="Weboldal", value="Hamarosan...")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["ei", "einfo", "emojii", "emoteinfo"], usage=",emojiinfo [emoji (alap discordos emojit a bot nem fogad el)]")
    async def emojiinfo(self, ctx, emoji: discord.Emoji):
        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.NotFound:
            return await ctx.reply("Nem találtam ilyen emojit.", mention_author=False)
        is_managed = "Igen" if emoji.managed else "Nem"
        is_animated = "Igen" if emoji.animated else "Nem"
        # requires_colons = "Igen" if emoji.require_colons else "Nem"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        description = f"""
        **Alap:**
        **- Név:** {emoji.name}
        **- Id:** {emoji.id}
        **- URL:** [Letöltés]({emoji.url})
        **- Feltöltő:** {emoji.user.mention}
        **- Készült:** {creation_time}
        **- Formátum:** `<:{emoji.name}:{emoji.id}>`
        
        **Egyéb:**
        **- Animált:** {is_animated}
        **- Kezelt:** {is_managed}
        **- Szerver neve:** {emoji.guild.name}
        **- Szerver Id:** {emoji.guild.id}
        """
        embed = discord.Embed(
            title=f"**Emoji információk a ** `{emoji.name}` emojihoz",
            description=description,
            colour=0xFF9900,
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.client.process_commands(after)

    @commands.command()
    async def rgb(self, ctx, r, g, b):
        alma = "%02x%02x%02x" % int((r, g, b))
        await ctx.reply(alma, mention_author=False)

    @commands.command()
    async def allzene(self, ctx):
        await ctx.reply(f"**{len(self.client.voice_clients)}** hangcsatornán játszok zenét jelenleg!", mention_author=False)

    
    @commands.command()
    async def covid(self, ctx, *, countryName = None):
        try:
            if countryName is None:
                embed=discord.Embed(title="Használat: ```,covid [ország]```", colour=0xff0000, timestamp=ctx.message.created_at)
                await ctx.reply(embed=embed)
            else:
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
                embed2.add_field(name="**Aktív fertőzöttekí**", value=active, inline=True)
                embed2.add_field(name="**Korházban ápoltak**", value=critical, inline=True)
                embed2.add_field(name="**Mintavételek**", value=totalTests, inline=True)
                embed2.add_field(name="**Fertőzések egy millió emberből**", value=casesPerOneMillion, inline=True)
                embed2.add_field(name="**Halálesetek egy millió emberből**", value=deathsPerOneMillion, inline=True)
                embed2.add_field(name="**Tesztek egy millió emberből**", value=testsPerOneMillion, inline=True)
                embed2.set_thumbnail(url="https://cdn.discordapp.com/attachments/564520348821749766/701422183217365052/2Q.png")
                await ctx.reply(embed=embed2)
        except:
            embed3 = discord.Embed(title="Az API nem támogatja ezt az országot!", colour=0xff0000, timestamp=ctx.message.created_at)
            embed3.set_footer(text="Hiba történt!")
            await ctx.reply(embed=embed3)

    @commands.command(usage=",timer [idő(másodpercben)]", aliases=["time", "cdown", "countdown", "cd", "countd", "visszaszámláló", "visszaszamlalo"])
    async def timer(self, ctx, time):
        timeint = int(time)
        embed = discord.Embed(title="Visszaszámláló", color=0xFF9900, footer="Radon × Timer", description=f"A {timeint} másodperces visszaszámláló elindult!")
        embed2 = discord.Embed(title="Visszaszámláló", color=0xFF9900, footer="Radon × Timer", description=f"A visszaszámláló lejárt!")
        msg = await ctx.reply(embed=embed, mention_author=False)
        await asyncio.sleep(timeint)
        await msg.edit(embed=embed2)

    @commands.command(aliases=["támogatás", "donét"])
    async def donate(self, ctx):
        embed = discord.Embed(title="Támogatás", description="[Tovább a támogatáshoz!](https://paypal.me/scopsyyt)\nMit kapsz érte? :thinking:\n - Saját rang a support szerveren\n - Saját parancs\n - Saját emojik!\n - **[ÚJ]** Early Access a (még meg nem nyitott) Minecraft szerver lobbyjához!", color=0xa2332)
        await ctx.reply(embed=embed, mention_author=False)

    #@commands.command()
    #async def help(self, ctx):
    #    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter. Válassz a számokkal a parancsokért.\n<:rn_1:824948188049702982> - Alap parancsok\n<:radon_2:824948188115894282> - Moderációs parancsok\n <:radon_3:824948187734343691> - Zene parancsok\n<:radon_4:824948187969880074> - Fun parancsok\n<:radon_5:824948188045639690> - Szint rendszer\n<:radon_6:824948187587805205> - Economy\n<:radon_7:824949157394513950> - Anti rendszerek\n<:radon_8:824949157462147072> - Beállítható rendszerek\n<:radon_9:824949157298176010> - Rádiók\n<:radon_10:824949156963024957> - Whitelist\n<:radon_11:824949157298962452> - Keresés\n<:radon_12:824949157563334686> - GlobalChat", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #    asd = await ctx.reply(embed=embed)
    #    await asd.add_reaction("<:rn_1:824948188049702982>")
    #    await asd.add_reaction("<:radon_2:824948188115894282>")
    #    await asd.add_reaction("<:radon_3:824948187734343691>")
    #    await asd.add_reaction("<:radon_4:824948187969880074>")
    #    await asd.add_reaction("<:radon_5:824948188045639690>")
    #    await asd.add_reaction("<:radon_6:824948187587805205>")
    #    await asd.add_reaction("<:radon_7:824949157394513950>")
    #    await asd.add_reaction("<:radon_8:824949157462147072>")
    #    await asd.add_reaction("<:radon_9:824949157298176010>")
    #    await asd.add_reaction("<:radon_10:824949156963024957>")
    #    await asd.add_reaction("<:radon_11:824949157298962452>")
    #    await asd.add_reaction("<:radon_12:824949157563334686>")
    #    await asyncio.sleep(1)
    #    def check(reaction, user):
    #        return reaction.message.id == asd.id and user == ctx.author and str(reaction.emoji) == "<:rn_1:824948188049702982>" or str(reaction.emoji) == "<:radon_2:824948188115894282>" or str(reaction.emoji) == "<:radon_3:824948187734343691>" or str(reaction.emoji) == "<:radon_4:824948187969880074>" or str(reaction.emoji) == "<:radon_5:824948188045639690>" or str(reaction.emoji) == "<:radon_6:824948187587805205>" or str(reaction.emoji) == "<:radon_7:824949157394513950>" or str(reaction.emoji) == "<:radon_8:824949157462147072>" or str(reaction.emoji) == "<:radon_9:824949157298176010>" or str(reaction.emoji) == "<:radon_10:824949156963024957>" or str(reaction.emoji) == "<:radon_11:824949157298962452>" or str(reaction.emoji) == "<:radon_12:824949157563334686>"
    #    while True:
    #        try: 
    #            reaction, user = await self.client.wait_for("reaction_add", check=check, timeout=30)
    #            if str(reaction.emoji) == "<:rn_1:824948188049702982>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Alap", value=f"**,ping** `-` A bot pingjének megtekintése\n**,árfolyam [valuta]** `-` Az adott valuta árfolyamának megtekintése\n**,yt [keresendő kifejezés]** `-` Youtube keresés\n**,időjárás [falu/város]** `-` Az adott helyen lévő időjárás\n**,nsfw** `-` 18+-os képek megtekintése\n**,say [üzenet]** `-` A bot elküldi az általad küldött üzenetet\n**,embedsay [üzenet]** `-` A bot elküldi az általad küldött üzenetet embedben\n**,kutya** `-` Kutyás képek\n**,szerverek** `-` Szerverek számának megtekintése\n**,szavazás [szavazandó dolog]** `-` Szavazás létrehozása\n**,invite** `-` A bot meghívása\n**,support** `-` A support szerver meghívója\n**,kérdés [kérdés]** `-` A bot válaszol a kérdésedre \n**,userinfo [@említés]** `-` Említett felhasználó információijainak megtekintése\n**,szerverinfo** `-` Az adott szerver információijainak megtekintése\n**,ticket** `-` Ticket nyitás\n**,close** `-` Ticket bezárása\n**,mcskin [minecraft felhasználónév]** `-` Minecraft Skin megnézése\n", inline=False)
    #                    embed.add_field(name="‎", value="**,avatar [felhasználó]** `-` Felhasználó profilképének lekérése\n**,meme** `-` Küld egy mémet\n**,nevnap** `-` Mai névnap\n**,roleinfo [rang]** `-` Rang információk\n**,channelinfo [csatorna]** `-` Csatorna információk\n**,emojiinfo [emoji]** `-` Csatorna információk\n**,cat** `-` Cicás képek\n**,ascii [szöveg]** `-` Ascii rajz\n**,donate** `-` Támogatási információk\n**,guildicon** `-` Szerver ikonja\n**,timer** `-` Időzítő\n**,dm** - Üzenetküldés a felhasználónak\n**,zaszlo** `-` Találd ki a zászlót játék**,giveaway** `-` Nyereményjáték létrehozása\n**,reroll [#csatorna] [üzenet id]** `-` Nyereményjáték újrasorolása\n**,mansorsol [#csatorna] [üzenet id]** `-` Manuális nyereményjáték sorsolás", inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_2:824948188115894282>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Moderáció", value="**,ban [@felhasználó] (indok)** `-` Felhasználó kitiltása\n**,kick [@felhasználó] (indok)** `-` Felhasználó kidobása\n**,purge [üzenetek száma]** `-` Üzenetek törlése\n**,roleall [@rang]** `-` A szerver összes felhasználójára rang adás.\n**,removeall [@rang]** `-` A szerver összes felhasználójától rang elvétel.\n**,unban [@felhasználó]** `-` Felhasználó kitiltásának feloldása\n**,removerole [@felhasználó] [@rang]** `-` Felhasználótól rang elvétel\n**,addrole [@felhasználó] [@rang]** `-` Felhasználóhoz rang hozzáadás\n**,bypass [@felhasználó]** `-` A megadott felhasználót ignorálja az autó moderáció\n**,removebypass [@felhasználó]** `-` A megadott felhasználót eltávolítja az ignoráltak listájából\n", inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_3:824948187734343691>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Zene Parancsok", value="**,play [cím]** `-` Kívánt zene lejátszása youtuberól\n**,pause** `-` Zene szüneteltetése\n**,resume** `-` Zene folytatása\n**,pause** `-` Zene megállítása\n**,leave** `-` Bot kiléptetése a hangcsatornából\n**,loop [be/ki]** - Zene ismétlődésének be vagy kikapcsolása", inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_4:824948187969880074>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Fun", value=f"**,jóslás** `-` Jósol neked a bot\n**,kill [@említés] [utolsó üzenete]**** `-` Említett felhasználó meggyilkolása\n**,pofon [@említés]** `-` Említett felhasználó megpofozása\n**,meleg [@említés]** `-` Említtet felhasználó melegségének megtekintése\n**,coinflip** `-` Szimpla fej vagy írás\n**,hug [@említés]** `-` Említett felhasználó megölelése\n**,futóverseny [@említés]** `-` Futóverseny\n**,fight [@említés]** `-` Verekedés\n**,pénisz [@említés]** `-` Említett felhasználó nemi szerv méretének megtekintése\n**,kor **`-` A bot megtippeli hogy hány éves vagy\n**,rps [kő/papír/olló]** `-` Kő-papír-olló játék (teljesen random)\n**,magasság (@felhasználó)** `-` A bot megtippeli a magasságod", inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_5:824948188045639690>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Szint Rendszer", value=f'**,level [be/ki]** `-` Level rendszer be/ki kapcsolása \n**,rank** `-` Szinted megtekintése\n**,chignore [#szoba]** `-` Level rendszerből egy szoba kizárása', inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_6:824948187587805205>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Economy", value=f'**,work** `-` Dolgozás\n**,slut** `-` Ribanckodás\n**,crime** `-` Rablás\n**,balance** `-` Egyenleged megtekintése\n**,luck [összeg]** `-` Feltett összeg szerencséje\n**,hourly** `-` Órabér\n**,daily** `-` Napibér\n**,weekly** `-` Hetibér\n**,monthly** `-` Havibér', inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_7:824949157394513950>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Anti Rendszerek", value=f'**,antiinvite [be/ki]** `-` Az inviteokat letiltja\n**,antilink [be/ki]** `-` A linkeket letiltja\n**,antispam [be/ki]** `-` A spamelést letiltja')
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_8:824949157462147072>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Beállítható Rendszerek", value="**,reactrole [emoji (NEM NITRÓS!)] [@RANG] [Szöveg]** `-` Reakciós rangok beállítása\n**,setjoin [be/ki] [#szoba]** `-` Üdvözlő szoba beállítása\n**,setleave [be/ki] [#szoba]** `-` Kilépő szoba beállítása\n**,autorole [be/ki] [@rang]** `-` Autorole be/ki kapcsolása", inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_9:824949157298176010>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Rádiók", value="**,radio1** `-` Rádió1 élő\n**,freshfm** `-` FreshFM élő\n**,petofi** `-` Petőfi rádió élő\n**,kossuth** `-` Kossuth rádió élő\n**,retro** `-` Retró rádió élő\n**,radio88** `-` Rádió88 élő\n", inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_10:824949156963024957>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Whitelist", value=f'**,whitelist [be/ki]** `-` Whitelist be és ki kapcsolása\n**,whitelist [add/remove] [id]** `-` Felhasználó hozzáadása és eltávolítása a WhiteList rendszerből', inline=False)
    #                    await asd.edit(content=None, embed=embed)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #            elif str(reaction.emoji) == "<:radon_11:824949157298962452>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="Keresés", value=f'**,google [keresendő kifejezés]** `-` Google keresés\n**,picnode [keresendő kifejezés]** `-` PicNode keresés\n**,twitter [keresendő kifejezés]** `-` Twitter keresés\n**,pornhub [keresendő kifejezés]** `-` Pornhub keresés\n**,twitch [keresendő kifejezés]** `-` Twitch keresés', inline=False)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #                    await asd.edit(content=None, embed=embed)
    #            elif str(reaction.emoji) == "<:radon_12:824949157563334686>":
    #                    embed = discord.Embed(title="Parancslista", description="A bot összes parancsa előtt a `,` szerepel.\n[] - Kötelező paraméter\n() - Opcionális paraméter.", color=ctx.message.author.top_role.color, timestamp=datetime.datetime.utcnow())
    #                    embed.add_field(name="GlobalChat", value=f'**,setglobalchat [#csatorna]** `-` GlobalChat bekapcsolása\n**,gcrules** `-` GlobalChat szabályzat', inline=False)
    #                    await asd.remove_reaction(reaction, ctx.author)
    #                    await asd.edit(content=None, embed=embed)
    #            else: 
    #                break
    #        except asyncio.TimeoutError:
    #            await asd.delete()
    #            break

    @commands.command(aliases=["parancsok", "segítség", "commands", "cmd"], usage=",help")
    async def help(self, ctx, kategoria=None):
        embed=discord.Embed(title="Segítség", description="Szia! Ha kíváncsi vagy a parancsaimra, **[itt](https://radonbot.hu/commands)** tekintheted meg őket!\nHa egyéb kérdésed lenne keresd fel a fejlesztőket **[itt](https://dc.radonbot.hu)**.", color=0xe9b603, footer="Radon × Help", timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
        """if kategoria==None:
            embed.add_field(name="Alap parancsok", value=",help alap", inline=True)
            embed.add_field(name="Moderációs parancsok", value=",help mod", inline=True)
            embed.add_field(name="Zene parancsok", value=",help zene", inline=True)
            embed.add_field(name="Fun parancsok", value=",help fun", inline=True)
            embed.add_field(name="Szint rendszer", value=",help lvl", inline=True)
            embed.add_field(name="Pénz rendszer", value=",help economy", inline=True)
            embed.add_field(name="Filter rendszer", value=",help filter", inline=True)
            embed.add_field(name="Beállítható rendszer", value=",help setup", inline=True)
            embed.add_field(name="Rádiók", value=",help rádió", inline=True)
            embed.add_field(name="Whitelist rendszer", value=",help whitelist", inline=True)
            embed.add_field(name="Keresés", value=",help keresés", inline=True)
            embed.add_field(name="Globalchat", value=",help globalchat", inline=True)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() == "alap":
            embed.add_field(name="Alap", value=f"`,ping` **-** A bot pingjének megtekintése\n`,ido` **-** Kiírja ajelenlegi időt (Magyarországi időzóna)\n`,árfolyam [valuta]` **-** Az adott valuta árfolyamának megtekintése\n`,yt [keresendő kifejezés]` **-** Youtube keresés\n`,időjárás [falu/város]` **-** Az adott helyen lévő időjárás\n`,nsfw` **-** 18+-os képek megtekintése\n`,say [üzenet]` **-** A bot elküldi az általad küldött üzenetet\n`,embedsay [üzenet]` **-** A bot elküldi az általad küldött üzenetet embedben\n`,kutya` **-** Kutyás képek\n`,szerverek` **-** Szerverek számának megtekintése\n`,szavazás [szöveg]` **-** Szavazás létrehozása\n`,invite` **-** A bot meghívása\n`,support` **-** A support szerver meghívója\n`,kérdés [kérdés]` **-** A bot válaszol a kérdésedre \n`,userinfo [@felhasználó]` **-** Említett felhasználó információijainak megtekintése\n`,szerverinfo` **-** Az adott szerver információijainak megtekintése\n`,ticket` **-** Ticket nyitás\n`,close` **-** Ticket bezárása", inline=False)
            embed.add_field(name="\u200b", value="`,hiba [hiba]` **-** Hiba jelentése a fejlesztőknek.\n`,guildicon` **-** Lekéri a szerver ikonját.\n`,ido` **-** Jelenlegi idő megtekintése\n`,mcszerver [ip] [port]` **-** MC szerver adatainak lekérdezése\n`,bc` **-** BirodalomCraft szerver információjainak megtekintése\n`,radoncraft` **-** RadonCraft infók\n`,avatar [felhasználó]` **-** Felhasználó profilképének lekérése\n`,meme` **-** Küld egy mémet\n`,nevnap` **-** Mai névnap\n`,roleinfo [@rang vagy rang ID]` **-** Rang információk\n`,channelinfo [csatorna]` **-** Csatorna információk\n`,emojiinfo [emoji]` `-` Emoji információk (alap discord emojival nem működik\n`,cat` **-** Cicás képek\n`,ascii [szöveg]` **-** Ascii rajz\n`,donate` **-** Támogatási információk\n`,guildicon` **-** Szerver ikonja\n`,timer` **-** Időzítő\n`,dm` **-** Üzenetküldés a felhasználónak\n`,zaszlo` **-** Találd ki a zászlót játék\n`,giveaway` **-** Nyereményjáték létrehozása\n`,mansorsol [#csatorna] [üzenet id]` **-** Manuális nyereményjáték sorsolás", inline=False)
            embed.add_field(name="\u200b", value="`,közösosztó [szám1] [szám2]` **-** Közös osztó megkeresése\n`,avatar (@felhasználó)` **-** Lekéri a felhasználó profilképét.\n`,calc [szám1] [művelet: +|-|*|/|^] [szám2]` **-** Számolás. A '^' a hatványozás.\n`,reroll [#csatorna] [üzenet id]` **-** Nyereményjáték újrasorolása\n`,mcskin [eredetis név]` **-** Minecraft Skin megnézése")
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("moderacio", "mod", "moderáció", "moderácio", "moderació", "admin"):
            embed.add_field(name="Moderáció", value="~~`,purge [üzenetek száma]` **-** Üzenetek törlése~~ **ÁTDOLGOZÁS MIATT NEM ELÉRHETŐ**\n`,roleall [@rang]` **-** A szerver összes felhasználójára rang adás.\n`,removeall [@rang]` **-** A szerver összes felhasználójától rang elvétel.\n`,dm [@felhasználó] [üzenet]` **-** Privát üzenet írása a boton keresztül.\n`,slowmode [idő másodpercben]` **-** Lassítás beállítása a jelenlegi csatornán.\n`,unban [@felhasználó]` **-** Felhasználó kitiltásának feloldása\n`,removerole [@felhasználó] [@rang]` **-** Felhasználótól rang elvétel\n`,addrole [@felhasználó] [@rang]` **-** Felhasználóhoz rang hozzáadás\n`,bypass [@felhasználó]` **-** A megadott felhasználót ignorálja az autó moderáció\n`,removebypass [@felhasználó]` **-** A megadott felhasználót eltávolítja az ignoráltak listájából", inline=False)
            embed.add_field(name="\u200b", value="`,warn [említés] [indok]` **-** Felhasználó figyelmeztetése\n`,nick [említés] [név]` **-** Felhasználó nevének megváltoztatása\n`,lockdown [#csatorna]` **-** Lezárja a csatornát. Ha már le van zárva, feloldja.\n`,nickall [név]` **-** A szerver tagjainak nevének megváltoztatása\n`,unbanall` **-** Felhasználók tiltásának feloldása\n`,tempban [említés] [idő] [indok]` **-** Felhasználó időre tiltása\n`,mute/unmute [említés] [indok]` **-** Felhasználó némításának kezelése\n`,softban [felhasználó] [indok]` **-** Felhasználó kitiltása az üzeneteivel együtt\n`,ban [@felhasználó] (indok)` **-** Felhasználó kitiltása\n`,kick [@felhasználó] (indok)` **-** Felhasználó kidobása\n`,warn [@felhasználó] (indok)` **-** Felhasználó figyelmeztetése", inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("zene", "music", "muzsika"):
            embed.add_field(name="Zene parancsok", value="`,play [cím]` **-** Kívánt zene lejátszása youtuberól\n`,pause` **-** Zene szüneteltetése\n`,resume` **-** Zene folytatása\n`,pause` **-** Zene megállítása\n`,leave` **-** Bot kiléptetése a hangcsatornából\n`,loop [be/ki]` **-** Zene ismétlődésének be vagy kikapcsolása **[BÉTA!]**", inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() == "fun":
            embed.add_field(name="Fun", value=f"`,swim [@felhasználó]` **-** Úszóverseny.\n`,jóslás` **-** Jósol neked a bot\n`,iq (@felhasználó)` **-** Megméred a másik IQ-ját\n`,közösosztó [szám1] [szám2]` **-** Kiszámolja a két szám legnagyobb közös osztóját.\n`,game` **-** Sorsol egy játékot neked.\n`,ascii [szöveg]` **-** Szép szöveg uwu\n`,dice` **-** A dobókocka eldobása.\n`,kill [@említés] (utolsó szavai)` **-** Említett felhasználó meggyilkolása\n`,pofon [@említés]` **-** Említett felhasználó megpofozása\n`,gay [@említés]` **-** Említett felhasználó melegségének megtekintése (100% real)\n`,coinflip` **-** Érme feldobása\n`,hug [@említés]` **-** Említett felhasználó megölelése\n`,futóverseny [@említés]` **-** Usain Bolt roleplay\n`,fight [@említés]` **-** KSI roleplay\n`,pp [@említés]` **-** Említett felhasználó nemi szerv méretének megtekintése\n`,kor (@felhasználó)` **-** A bot megtippeli hogy hány éves vagy\n`,rps [kő/papír/olló]` **-** Kő-papír-olló játék (teljesen random)\n`,magasság (@felhasználó)` **-** A bot megtippeli a magasságod", inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("lvl", "szint", "level"):
            embed.add_field(name="Szint rendszer", value=f'`,level [be/ki]` **-** Szint rendszer be/ki kapcsolása \n`,rank` **-** Szinted megtekintése\n`,chignore [#szoba]` **-** Level rendszerből egy szoba kizárása', inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("economy", "eco", "pénz", "penz", "pénzrendszer", "penzrendszer"):
            embed.add_field(name="Economy", value=f'`,work` **-** Dolgozás\n**,slut** `-` Ármándózás\n`,crime` **-** Rablás\n`,balance` **-** Egyenleged megtekintése\n`,luck [összeg]` **-** Feltett pénz nyerése vagy elvesztése (25% nyerési esély)\n`,gnum` **-** 10 lehetőséged van kitalálni egy 1 és 100 közötti random számot. Ha eltalálod, nyersz 300 RC-t.\n`,hourly` **-** Órabér\n`,daily` **-** Napibér\n`,weekly` **-** Hetibér\n`,monthly` **-** Havibér', inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("filter", "anti"):
            embed.add_field(name="Filter rendszer", value=f'`,antiinvite [be/ki]` **-** Az inviteokat letiltja\n`,antilink [be/ki]` **-** A linkeket letiltja\n`,antispam [be/ki]` **-** A spamelést letiltja')
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() == "setup":
            embed.add_field(name="Beállítható rendszer", value="`,reactrole [emoji (NEM NITRÓS!)] [@rang vagy rang ID] [szöveg]` **-** Reakciós rangok beállítása\n`,setjoin [be/ki] [#szoba]` **-** Üdvözlő szoba beállítása\n`,setleave [be/ki] [#szoba]` **-** Kilépő szoba beállítása\n`,autorole [be/ki] [@rang]` **-** Autorole be/ki kapcsolása", inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("radio", "rádió", "radió", "rádio"):
            embed.add_field(name="Rádiók", value="`,radio1` **-** Rádió1 élő\n`,freshfm` **-** FreshFM élő\n`,petofi` **-** Petőfi rádió élő\n`,kossuth` **-** Kossuth rádió élő\n`,retro` **-** Retró rádió élő\n`,radio88` **-** Rádió88 élő\n", inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("whitelist", "fehérlista"):
            embed.add_field(name="Whitelist", value=f'`,whitelist [be/ki]` **-** Whitelist be és ki kapcsolása\n`,whitelist [add/remove] [id]` **-** Felhasználó hozzáadása és eltávolítása a WhiteList rendszerből', inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() in ("search", "keresés", "kereses"):
            embed.add_field(name="Keresés", value=f'`,google [keresendő kifejezés]` **-** Google keresés\n`,picnode [keresendő kifejezés]` **-** PicNode keresés\n`,twitter [keresendő kifejezés]` **-** Twitter keresés\n||`,pornhub [keresendő kifejezés]` **-** Pornhub keresés||\n`,twitch [keresendő kifejezés]` **-** Twitch keresés', inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        elif str(kategoria).lower() == "globalchat":
            embed.add_field(name="GlobalChat", value=f'`,setglobalchat [#csatorna]` **-** GlobalChat bekapcsolása\n`,gcrules` **-** GlobalChat szabályzat', inline=False)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            await ctx.reply("Hibás paraméter!", mention_author=False)"""

    @commands.command(aliases=["botinfo", "bot-info", "binfo", "bi", "boti"])
    async def botinfó(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        channelCount = len(set(self.client.get_all_channels()))
        embed = discord.Embed(title=f"Bot információ", description="A Radon bot információi", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Bot neve", value="Radon", inline=True)
        embed.add_field(name="Készült", value="2021.02.03", inline=True)
        embed.add_field(name="Programozási könytár", value="discord.py")
        embed.add_field(name="Szerverek", value=f"{serverCount}")
        embed.add_field(name="Csatornák", value=f"{channelCount}")
        embed.add_field(name="Felhasználók", value=f"{memberCount}")
        embed.add_field(name="Python verzió", value=f"{pythonVersion}")
        embed.add_field(name="Parancsok száma", value=f"{len(self.client.commands)}")
        embed.add_field(name="discord.py verzió", value=f"{dpyVersion}")
        embed.add_field(name="Operációs rendszer", value=f"Linux Ubuntu 20.04")
        embed.add_field(name="CPU-k típusa", value="Intel® Xeon® X5650")
        embed.add_field(name="CPU-k száma", value=f"{psutil.cpu_count()} db")
        embed.add_field(name="CPU-k teljesítménye", value="2.67GHz")
        embed.add_field(name="Memória mérete", value=f"4 GB")
        embed.add_field(name="CPU kihasználtság", value=f"{psutil.cpu_percent()}%")
        embed.add_field(name="Memória kihasználtság", value=f"{psutil.virtual_memory().percent}%")
        await ctx.reply(embed=embed, mention_author=False)
            
    @commands.command(aliases=["allmember", "össztag", "members", "tagok", "tag"])
    async def alltag(self, ctx):
        embed = discord.Embed(title="Felhasználók", description=f"A bot összes szerverén lévő felhasználók száma: **{len(set(self.client.get_all_members()))}**", timestamp=datetime.datetime.utcnow(), color=0xFF9900)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["javaslat", "javasol", "otlet", "suggestion"], usage=",ötlet <szöveg>")
    @commands.cooldown(1, 600, type=commands.BucketType.user)
    async def ötlet(self, ctx, *, message1):
        if ctx.author.id == 507577389040271374:
            await ctx.reply("Nem használhatod ezt a parancsot!", mention_author=False)
            return
        channel = self.client.get_channel(806906693191073862)
        await ctx.reply("<:radon_pipa:811191514369753149> Sikeresen elküldtem a javaslatod!", mention_author=False)
        embed = discord.Embed(title="Javaslat", description=f"{ctx.author} ötletet írt!", color=0x0f3f)
        embed.add_field(name="Ötlet:", value=f"```{message1}```")
        embed.set_footer(text=f"Radon × Javaslat", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        message = await channel.send(embed=embed)
        await message.add_reaction('<:radon_pipa:811191514369753149>')
        await message.add_reaction('<:radon_x:811191514482212874>')

    @commands.command(aliases=["bug", "bugreport", "hibareport", "hibajelentes", "hibajelentés"], usage=",hiba [szöveg (FIGYELEM: írd le a hibát, hogy mikor vetted észre, hogy hogyan idézted elő!)]")
    @commands.cooldown(1, 60, type=commands.BucketType.user)
    async def hiba(self, ctx, *, message1):
        if ctx.author.id == 507577389040271374:
            await ctx.reply("Nem használhatod ezt a parancsot!", mention_author=False)
            return
        channel = self.client.get_channel(832914321230266398)
        await ctx.reply("<:radon_pipa:811191514369753149> Sikeresen elküldtem a hibát!", mention_author=False)
        embed = discord.Embed(title="Hibajelentés!", description=f"{ctx.author} hibát jelentett!\nReagálj pipával, ha elő tudod idézni.\nReagálj X-szel, ha nem tudod előidézni.", color=0xff0000, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Hiba:", value=f"```{message1}```")
        embed.set_footer(text=f"Radon × Hiba", icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await channel.send("@here")
        message = await channel.send(embed=embed)
        await message.add_reaction('<:radon_pipa:811191514369753149>')
        await message.add_reaction('<:radon_x:811191514482212874>')

#    @commands.command(aliases=["pong", "connection", "net", "network"])
#    async def ping(self, ctx):
#        before = time.monotonic()
#        message = await ctx.reply("<:radon_toltes:811192219579056158> Pingelés...")
#        try:
#            ping = round((time.monotonic() - before) * 1000)
#            before2=time.monotonic()
#            cursor = db.cursor()
#            cursor.execute("SELECT * FROM rc")
#            cursor.fetchall()
#            db.commit()
#            ping2 = round((time.monotonic() - before2) * 1000)
#            embed = discord.Embed(title=":ping_pong: Pong!", description=f"Üzenetküldés ideje: `{ping}`ms\nBot pingje: `{round(self.client.latency * 1000)}ms`\nAdatbázis ping: `{ping2}ms`", color=0xFF9900, timestamp=datetime.datetime.utcnow())
#            embed.set_author(name=f"Ping × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
#            await message.edit(content=None, embed=embed)
#        except:
#            embed = discord.Embed(title=":ping_pong: Pong!", description=f"Üzenetküldés ideje: `{ping}`ms\nBot pingje: `{round(self.client.latency * 1000)}ms`\nAdatbázis ping: `Nem tudtam lekérni`", color=0xFF9900, timestamp=datetime.datetime.utcnow())
#            embed.set_author(name=f"Ping × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
#            await message.edit(content=None, embed=embed)

    @commands.command(usage=",aliases [parancs]", aliases=["alias", "al"])
    async def aliases(self, ctx, command):
        command = command.lower()
        try: command = self.client.get_command(command)
        except: await ctx.reply("Nem található ilyen parancs!", mention_author=False)
        aliases = command.aliases
        if aliases == None: 
            await ctx.reply("Nem található alias ennél a parancsnál!", mention_author=False)
            return
        a = ""
        for aliases in command.aliases:
            a = a + aliases + "\n"
        embed = discord.Embed(description=f"{command.name}\n{a}", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"Aliases × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)     
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",árfolyam [valuta]", aliases=["exchange", "exch", "ár", "arfolyam"])
    async def árfolyam(self, ctx, valasz):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15', "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
        if valasz == "euro" or valasz == "euró":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=maF&sxsrf=ALeKk01GxrywcQOrodL7Fm-sLksgl64Shw%3A1602246229608&ei=VVaAX4PXJIKNrwT4j7_IBg&q=1+eur+to+huf&oq=1+eur&gs_lcp=CgZwc3ktYWIQARgAMgkIIxAnEEYQggIyBAgAEEMyBQgAELEDMgQIABBDMgUIABDLATIECAAQQzICCAAyAggAMgQIABBDMgUIABDLAToHCCMQ6gIQJzoECCMQJzoICAAQsQMQgwE6BQguELEDOgIILjoHCAAQsQMQQ1DxFFiXLmD9PGgCcAF4AIABhQGIAaAFkgEDMi40mAEAoAEBqgEHZ3dzLXdperABCsABAQ&sclient=psy-ab", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for euroget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                euro = euroget.get_text()
                await ctx.reply(f"Euró árfolyama: {euro} Forint", mention_author=False)
        elif valasz == "btc" or valasz == "bitcoin":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=vaF&sxsrf=ALeKk00wKOHMmYX9YbgjmG-NkeZRr9nCiw%3A1602246238253&ei=XlaAX-XwDpC53AOmqLSYDA&q=1+btc+to+huf&oq=1+btc+to+huf&gs_lcp=CgZwc3ktYWIQAzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJzIHCCMQ6gIQJ1CEuwlY29YJYPzYCWgBcAF4AIABAIgBAJIBAJgBAKABAaoBB2d3cy13aXqwAQrAAQE&sclient=psy-ab&ved=0ahUKEwjll_6uwKfsAhWQHHcKHSYUDcMQ4dUDCAw&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Bitcoin árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "font":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=9xu&sxsrf=ALeKk009xKR-xdop5rncHbISYrvbiCIxEQ%3A1602246400840&ei=AFeAX8HoMumRrgST67roBg&q=1+font+to+huf&oq=1+font+to+huf&gs_lcp=CgZwc3ktYWIQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjICCAAyBggAEAcQHjIGCAAQBxAeMgYIABAHEB46BAgAEEc6BwgjELACECc6BAgAEA1QqIoIWMSTCGCllAhoAHACeACAAZ0BiAGBB5IBAzIuNpgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjB6MH8wKfsAhXpiIsKHZO1Dm0Q4dUDCAw&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Font árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "dollár":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?client=opera-gx&hs=K0u&sxsrf=ALeKk00Bsb7nZx9atsV8v9nB6QZLGDy-pA%3A1602246535532&ei=h1eAX4zzH-qFrwSZ2JLYCQ&q=1+dollar+to+huf&oq=1+dollar+to+huf&gs_lcp=CgZwc3ktYWIQAzIJCCMQJxBGEIICMgYIABAHEB4yBggAEAgQHjIGCAAQCBAeMgYIABAIEB4yBggAEAgQHjIGCAAQCBAeOgwIIxCwAhAnEEYQggI6CAgAEAgQDRAeOgcIIxCwAhAnOggIABAIEAcQHlD1DVilFmD2F2gCcAB4AIABbogB0gGSAQMwLjKYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab&ved=0ahUKEwjM0t68wafsAhXqwosKHRmsBJsQ4dUDCAw&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Dollár árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "frank":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?q=1+dfrank+to+huf&oq=1+dfrank+to+huf&aqs=chrome..69i57j0.5659j1j1&sourceid=chrome&ie=UTF-8", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Frank árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "jen":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01uFnBZQJJ0Ty25OzbnSdcD-Q0XdA%3A1602335304083&ei=SLKBX76qBO_2qwHElJ6ABg&q=1+jen+to+huf&oq=1+jen+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQCjoECAAQRzoFCAAQzQI6BggAEAcQHlCnkUxYkqVMYLiqTGgBcAF4AIABugGIAfUJkgEDMS45mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwi-7vCUjKrsAhVv-yoKHUSKB2AQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Jen árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "lej":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk00pxEYx683QkRL5LubbRDzC9kU54g%3A1602336556855&ei=LLeBX9vVM-THrgS83KzIDA&q=1+lej+to+huf&oq=1+lej+to+huf&gs_lcp=CgZwc3ktYWIQAzICCAA6BAgAEEc6CAgAEAcQChAeOgYIABAHEB5Qp8sKWOnUCmCP2gpoAHACeACAAXuIAfgEkgEDMS41mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjbm6DqkKrsAhXko4sKHTwuC8kQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Lej árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "zloty":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk03SGXdbVi35OECDeJA_J_SC8L21Dg%3A1602336735222&ei=37eBX9CHDafIrgTGnquYAw&q=1+zloty+to+huf&oq=1+zloty+to+huf&gs_lcp=CgZwc3ktYWIQAzICCAA6BAgAEEc6BggAEAcQHjoICAAQBxAKEB46BAgAEB46BAgAEA06CAgAEAgQDRAeUObXClii5Qpg4ucKaABwA3gAgAF2iAGJBpIBAzUuM5gBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwiQ86a_karsAhUnpIsKHUbPCjMQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Zloty árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "kuna":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk02Yz7o-BdwSvMPmapqMdRJsROG5pw%3A1602336914232&ei=kriBX8rRDdL3qwH-uJPYCA&q=1+kuna+to+huf&oq=1+kuna+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQQzoECAAQRzoHCCMQsAIQJzoECAAQDToICAAQCBANEB46AggAOgYIABAHEB5QzPQGWIqCB2CzhAdoAHACeACAAXaIAcIHkgEDMy42mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjK4tSUkqrsAhXS-yoKHX7cBIsQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Kuna árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "dinár":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01a9laB5ypw4GYi_5CtWct6DcLmjg%3A1602337030781&ei=BrmBX-KbL-LGrgTN6JnoBQ&q=1+din%C3%A1r+to+huf&oq=1+din%C3%A1r+to+huf&gs_lcp=CgZwc3ktYWIQAzICCAA6BAgAEEc6BwgjELECECc6BwgjELACECc6BggAEAcQHjoECAAQDToICAAQCBAHEB46BwgAEEYQggI6CAgAEAgQDRAeUMy8Cljtygpg6cwKaABwAngAgAGZAYgB9QeSAQMyLjeYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab&ved=0ahUKEwjitp7MkqrsAhVio4sKHU10Bl0Q4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Dinár árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "líra":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk020U2iY6SGaYzoWwgfGM5uwKgnsog%3A1602337325847&ei=LbqBX8OnM4rurgTK7am4Dw&q=1+l%C3%ADra+to+huf&oq=1+l%C3%ADra+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQIyBQgAEM0CMgUIABDNAjIFCAAQzQIyBQgAEM0COgQIABBHOgYIABAHEB46CAgAEAcQChAeOgQIABAeOgQIABANOggIABAIEA0QHlCd2gZYgegGYIbrBmgBcAJ4AIABb4gBuASSAQM0LjKYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab&ved=0ahUKEwiD8vfYk6rsAhUKt4sKHcp2CvcQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Líra árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "peso":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk03qdVi3NaIrSwZlAUtSIyoRRx9EKQ%3A1602337438793&ei=nrqBX-HzL8borgTA3bGICg&q=1+peso+to+huf&oq=1+peso+to+huf&gs_lcp=CgZwc3ktYWIQAzIHCAAQRhCCAjIGCAAQCBAeOgQIABBHOgQIABANOggIABAIEA0QHjoFCAAQzQI6BggAEAcQHjoICAAQBxAKEB46CAgAEAgQBxAeUIGzB1ijxQdghMgHaABwA3gAgAF_iAHXBpIBAzMuNZgBAKABAaoBB2d3cy13aXrIAQjAAQE&sclient=psy-ab&ved=0ahUKEwjhuuWOlKrsAhVGtIsKHcBuDKEQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Peso árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "hrivnya":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01Ykv6FWIMPrvFVmcklFq-3kVV1cA%3A1602337564119&ei=HLuBX43jBoeOrwTV26-ADQ&q=1+hvrinya+to+huf&oq=1+hvrinya+to+huf&gs_lcp=CgZwc3ktYWIQAzIJCAAQDRBGEIICOgQIABBHOgcIIxCwAhAnOgYIABAHEB46CAgAEAgQBxAeOgIIADoECAAQDVCO2AVYsO0FYKP6BWgAcAJ4AIABhgGIAYAJkgEDNC43mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwiN4cbKlKrsAhUHx4sKHdXtC9AQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Hrivnya árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "rúpia":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk03_H08c6tbuNpSXHabRn5kFt-b1EA%3A1602337731517&ei=w7uBX9r6HpKyrgSvpaLADQ&q=1+r%C3%BApia+to+huf&oq=1+r%C3%BApia+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQHjoECAAQRzoGCAAQDRAeOgYIABAHEB46BAgAEA1QjyRYjDRg0TVoAHACeACAAXeIAccGkgEDMy41mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwia6K-alarsAhUSmYsKHa-SCNgQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Rúpia árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "riál":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk01eeRUthMDtd5cf5lRgA_XyLyRgpg%3A1602337740134&ei=zLuBX_fjB8T9rgTgqq9w&q=1+ri%C3%A1l+to+huf&oq=1+ri%C3%A1l+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQI6BAgAEEc6BwgjELACECc6BAgAEA06BggAEAcQHjoJCAAQDRBGEIICOggIABAIEAcQHlCyoARY3rAEYL22BGgBcAJ4AIABeYgBnQaSAQM1LjOYAQCgAQGqAQdnd3Mtd2l6yAEIwAEB&sclient=psy-ab&ved=0ahUKEwj3-b2elarsAhXEvosKHWDVCw4Q4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Riál árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "rubel":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk014NZhiDGl3w7o-R-z50KxcaKrIIg%3A1602337814143&ei=FryBX-KgCM3orgS-972gDg&q=1+rubel+to+huf&oq=1+rubel+to+huf&gs_lcp=CgZwc3ktYWIQAzIECAAQCjoECAAQRzoFCAAQzQI6BAgAEA06CAgAEAgQBxAeOgYIABAHEB46CQgAEA0QRhCCAjoHCAAQRhCCAjoICAAQBxAKEB5QsroEWN7IBGC7zARoAHACeACAAXaIAeEFkgEDMS42mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjig-PBlarsAhVNtIsKHb57D-QQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Rubel árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "sol":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk02VEjr_hmh7xLaHblNlVDEYyXx2Qw%3A1602337890576&ei=YryBX8HLIuz1qwGax7HwAg&q=1+sol+to+huf&oq=1+sol+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQIyBQgAEM0CMgUIABDNAjoECAAQRzoICAAQBxAKEB46AggAOgYIABAHEB46BAgAEA1Q3NICWKfmAmCE6QJoAHACeACAAWaIAewFkgEDNy4xmAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjBhJzmlarsAhXs-ioKHZpjDC4Q4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Sol árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "afgán":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?q=1+afg%C3%A1n+to+huf&oq=1+afg%C3%A1n+to+huf&aqs=chrome..69i57j0i333l3.4468j0j7&sourceid=chrome&ie=UTF-8", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Afgán árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "kwanza":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk02xGhUfwFcVdHpD0RWI0OWEaKce9g%3A1603016418670&ei=4haMX6adKJ2GwPAP-aihwAs&q=1+kwanza+to+huf&oq=1+kwanza+to+huf&gs_lcp=CgZwc3ktYWIQAzoECAAQRzoFCAAQzQI6BAgAEA06CQgAEA0QRhCCAjoGCAAQBxAeOggIABAIEAcQHlCqkRtYor0bYKm-G2gBcAJ4AIABnQKIAb8LkgEFNS42LjGYAQCgAQGqAQdnd3Mtd2l6yAEFwAEB&sclient=psy-ab&ved=0ahUKEwimltDB9b3sAhUdAxAIHXlUCLgQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Kwanza árfolyama: {btc} Forint", mention_author=False)
        elif valasz == "lek":
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.google.com/search?sxsrf=ALeKk00_xKUkqqvjlYkHOa0-175-la2zlw%3A1603031117569&ei=TVCMX4aiIvHIrgTjkrrgAg&q=1+leke+to+huf&oq=1+leke+to+huf&gs_lcp=CgZwc3ktYWIQAzIFCAAQzQI6BAgAEEc6BggAEAcQHjoICAAQBxAKEB46BAgjECdQgzBYgjVguzZoAHACeACAAWyIAf0DkgEDMS40mAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=psy-ab&ved=0ahUKEwjG_M2irL7sAhVxpIsKHWOJDiwQ4dUDCA0&uact=5", headers=headers) as r:
                    resp = await r.text()
            import bs4
            soup = bs4.BeautifulSoup(resp, features="html.parser")
            for btcget in soup.find_all('span', {"class": "DFlfde SwHCTb"}):
                btc = btcget.get_text()
                await ctx.reply(f"Lek árfolyama: {btc} Forint", mention_author=False)
        else:
            await ctx.reply("Nincs ilyen választási lehetőség! Választási lehetőségek: dollár, euró (vagy euro), bitcoin (vagy btc), font, frank, jen, lej, zloty, kuna, dinár, líra, peso, hrivnya, rúpia, riál, rubel, kwanza, lek afgán vagy sol.", mention_author=False)

    @commands.command(usage=",youtube [videó cím]", aliases=["youtube", "ytkeresés", "ytsearch"])
    async def yt(self, ctx, *, search):
        import re
        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
        link = 'http://www.youtube.com/watch?v=' + search_results[0]
        embed = discord.Embed( description=f"A legelső találat a következő. Link: {link}", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"Youtube × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)   
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
                if weather_description == "shower rain":
                    a = "Záporeső"
                elif weather_description == "broken clouds":
                    a = "Felszakadozott felhőzet"
                elif weather_description == "haze":
                    a = "Köd"
                elif weather_description == "few clouds":
                    a = "Kevés felhő"
                elif weather_description == "mist":
                    a = "Köd"
                elif weather_description == "clear sky":
                    a = "Tiszta ég"
                elif weather_description == "cattered clouds":
                    a = "Szétszórt felhőzet"
                elif weather_description == "fog":
                    a="Köd"
                elif weather_description == "rain":
                    a = "Eső"
                elif weather_description == "thunderstorm":
                    a = "Vihar"
                elif weather_description == "snow":
                    a = "Hó"
                elif weather_description == "light rain":
                    a = "Eső"
                elif weather_description == "overcast clouds":
                    a = "Borult felhők"
                else:
                    embed = discord.Embed(description="Nem tudtam lekérni az időjárást! Kérlek próbáld meg később!<:radon_x:811191514482212874> ", color=0xff0000, timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)
                embed = discord.Embed(title="Időjárás", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="Leírás", value=f"**{a}**", inline=False)
                embed.add_field(name="Fok(C)", value=f"**{current_temperature_celsiuis}°C**", inline=False)
                embed.add_field(name="Páratartalom(%)", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(name="Légköri Nyomás(hPa)", value=f"**{current_pressure}hPa**", inline=False)
                embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
                embed.set_author(name=f"Időjárás itt: {city_name} × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)   
                await xd.edit(embed=embed)
        else:
            embed = discord.Embed(description="Nem található város, vagy nincs adat erről a városról!<:radon_x:811191514482212874> ", color=0xff0000, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)



    @commands.command(usage=",say [üzenet]")
    async def say(self, ctx, *, message):
        if ctx.author.guild_permissions.manage_messages:
            if not ctx.message.author.bot:
                if ctx.message.mentions: 
                    await ctx.reply("Nem pingelhetsz az üzenetben!", mention_author=False)
                    return
                
                if "discord.gg" in message: 
                    await ctx.reply("Nem hírdethetsz az üzenetben!", mention_author=False)
                    return
                if "discord.com" in message: 
                    await ctx.reply("Nem hírdethetsz az üzenetben!", mention_author=False)
                    return
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
            embed.set_author(name=f"Embedsay × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(usage=",coloresay [üzenet] [HEX színkód]", aliases=["coloresay","colorembeds", "colorembed", "saycolorembed", "colore", "cembed", "colorembedsay"])
    async def ce(self, ctx, color1, *, message):
        if not ctx.message.author.bot:
            await ctx.message.delete()
            embed = discord.Embed(description=message, color=color1, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Embedsay × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)


    @commands.command(aliases=["server", "servers", "szerver", "szerverszám"])
    async def szerverek(self, ctx):
        servers = len(self.client.guilds)
        embed = discord.Embed(title="Szerverek száma", description=f"A bot jelenleg {servers} szerveren elérhető!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Szerverek × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",szavazás [üzenet]", aliases=["szavazas", "vote", "poll"])
    async def szavazás(self, ctx, *, msg):
            await ctx.message.delete()
            embed = discord.Embed(title="Szavazás", description="{}".format(msg), color = 0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Szavazás × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            message = await ctx.send(embed=embed)
            await message.add_reaction('<:radon_pipa:811191514369753149>')
            await message.add_reaction('<:radon_x:811191514482212874>')

    @commands.command(aliases=["meghív"])
    async def invite(self, ctx):
            embed = discord.Embed(title="Meghívás", description="A bot meghívásához [**kattints ide!**](https://discord.com/api/oauth2/authorize?client_id=713014602891264051&permissions=8&scope=bot)", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Meghívás × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def support(self, ctx):
        if not ctx.message.author.bot:
            embed = discord.Embed(title="Support szerver", description="A support szerverre való belépéshez [**kattints ide!**](https://discord.gg/QGnNVQk8Xs)", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Support × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",kérdés [kérdésed]", aliases=["kerdes", "question", "8ball"])
    async def kérdés(self, ctx, *,message1):
        kérdés = ['Igen',
                'Nem',
                'Nem tudom',
                'Biztosan',
                'Kérdezz valaki mást...',
                'Esélyes',
                'Esélytelen',
                'Nem valószínű']
        if not ctx.message.author.bot:
            embed = discord.Embed(title="A bot azt mondja...", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Kérdés × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            embed.add_field(name="Kérdés", value=message1)
            embed.add_field(name="Válasz", value=random.choice(kérdés))
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["ui","useri","uinfo", "uf", "ufind", "userfind", "usersearch", "us", "usearch"], usage=",userinfo [felhasználó]")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        embed = discord.Embed(title="Felhasználó információi", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"Kérte: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Beceneve", value=member.display_name)
        embed.add_field(name="Név#Tag", value=f"{member.name}#{member.discriminator}")
        embed.add_field(name="Fiókját létrehozta", value=str(member.created_at).replace("-", ". "))
        embed.add_field(name="A szerverre belépett", value=str(member.joined_at).replace("-", ". "))
        embed.add_field(name="Legmagasabb rangja", value=member.top_role.mention)
        if str(member.status).title() == None:
            a = "Nincs státusza"
        else: a = str(member.status).title()
        embed.add_field(name="Státusza", value=a)
        try:
            embed.add_field(name="Aktivitása", value=f"{str(member.activity.type).split('.')[-1].title()}: {member.activity.name}")
        except:
            embed.add_field(name="Aktivitása", value=f"Nincs megadva")
        if member.bot == True:
            a = "Igen"
        else:
            a = "Nem"
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
        embed.set_footer(text=f"Kérte: {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="ID", value=ctx.guild.id)
        embed.add_field(name="Tulajdonos", value=ctx.guild.owner)
        embed.add_field(name = "Nitro boostok száma", value = f"{ctx.guild.premium_subscription_count}", inline = True)
        embed.add_field(name = "Nitro boost szintje", value = f"{ctx.guild.premium_tier}", inline = True)
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
        embed.add_field(name="Státuszok", value= f"{statuses[0]}🟢 {statuses[1]}🟡 {statuses[2]}🔴 {statuses[3]}⚪")
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

    @commands.command(aliases=["emojisteal", "forkemoji", "emojifork", "fork_emoji"], usage=",stealemoji [emoji neve]")
    async def stealemoji(self, ctx, emojiname):
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

def setup(client):
    client.add_cog(Basic(client))

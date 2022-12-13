import discord
from discord.ext import commands
import datetime
import random
import asyncio
import requests
import aiohttp
import asyncio
import urllib

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=",iq (@felhasználó)")
    async def iq(self, ctx, member=None):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if member == None:
            embed = discord.Embed(description=f"{ctx.author.mention} IQ-ja: **{random.randint(60, 230)}** IQ pont. Büszkék vagyunk rád.", color=0xe9b703, ítimestamp=datetime.datetime.utcnow())
            embed.set_author(name="IQ", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × IQ", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"{member.mention} IQ-ja: **{random.randint(60, 170)}** IQ pont. Büszkék vagyunk rád.", color=0xe9b703, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="IQ", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × IQ", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",randomszám [szám1] [szám2]")
    async def randomszám(self, ctx, szam1: int, szam2: int):
        vegsoszam = random.randint(szam1, szam2)
        await ctx.reply(content=f"A random szám: **{vegsoszam}**!", mention_author=False)

    @commands.command(usage=",age (@felhasználó)",aliases=["kor", "életkor", "eletkor"])
    async def age(self, ctx, member=None):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        age = random.randint(1, 100)
        if member == None:
            embed = discord.Embed(description=f"A te életkorod: {age} év", color=0xe9b703, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Életkor", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Életkor", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(title="Életkor mérő", description=f"{member} kora: {age} év", color=0xe9b703, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Életkor", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Életkor", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def p4tr1k(self, ctx):
        await ctx.reply(content="P4TR1K on top!", mention_author=False)

    @commands.command(usage=",pp (@felhasználó)",aliases=["kuki", "farok", "dick", "cock", "penisz", "pp"])
    async def pénisz(self, ctx, member=None):
        dicks = ['8=D',
                '8==D',
                '8===D',
                '8====D',
                '8=====D',
                '8======D',
                '8=======D',
                '8========D']
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if member == None:
            embed = discord.Embed(description=f"E-Péniszed hossza: {random.choice(dicks)}", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Méret", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Méret", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"{member.mention} e-pénisze: {random.choice(dicks)}", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Méret", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Méret", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",cici (@felhasználó)",aliases=["mell", "csöcs", "domborzat", "uncode", "uc"])
    async def cici(self, ctx, member=None):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        dicks = ['(.)(.)',
                '(. )( .)',
                '( . )( . )',
                '( . ‏‏‎ ‎)(‏‏‎ ‎ . )',
                '( . ‏‏‎ ‎) (‏‏‎ ‎ . )',
                '(‏‏‎ ‎ . ‏‏‎ ‎) (‏‏‎ ‎ . ‏‏‎ ‎)',
                '(‏‏‎ ‎‏‏‎ ‎.‏‏‎ ‎ ‏‏‎ ‎) (‏‏‎ ‎ ‏‏‎ ‎.‏‏‎ ‎‏‏‎ ‎)',
                '(‏‏‎ ‎‏‏‎ ‎.‏‏‎ ‎ ‏‏‎ ‎)‏‏‎ ‎ (‏‏‎ ‎ ‏‏‎ ‎. ‏‏‎ ‎)']
        if member == None:
            embed = discord.Embed(description=f"E-Csöcsöd mérete: {random.choice(dicks)}", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Méret", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Méret", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"E-Csöcsöd mérete: {member.mention}-nak/nek: {random.choice(dicks)}", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name="Méret", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Méret", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",magasság [@felhasználó]",aliases=["magassag", "height", "mag", "cm"])
    async def magasság(self, ctx, member=None):
        a = random.randint(100, 250)
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        if member==None:
            embed = discord.Embed(description=f"Magasságod: {a}", timestamp=datetime.datetime.utcnow(), color=0xe9b603)
            embed.set_author(name="Magasság", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Magasság", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"{member.mention} magassága: {a}", timestamp=datetime.datetime.utcnow(), color=0xe9b603)
            embed.set_author(name="Magasság", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Magasság", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["zászló"])
    async def zaszlo(self, ctx):
        path = ["Zaszlo1", "Zaszlo2", "Zaszlo3", "Zaszlo4", "Zaszlo5", "Zaszlo6", "Zaszlo7", "Zaszlo8", "Zaszlo9", "Zaszlo10", "Zaszlo11", "Zaszlo12", "Zaszlo13", "Zaszlo14", "Zaszlo15", "Zaszlo16", "Zaszlo18", "Zaszlo19", "Zaszlo20", "Zaszlo21"]
        orszag = random.choice(path)
        await ctx.reply(content="A játék elindult. 2 perced lesz válaszolni, a választ __prefix nélkül__ a chatbe írdd. Az ország a következő:", file=discord.File(f'./zaszlok/{orszag}.png'), mention_author=False)
        def check(message): return message.channel == ctx.channel and message.author == ctx.author and message.guild == ctx.guild
        try: valasz = await self.client.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError: await ctx.send("Nem válaszoltál időben! A játék véget ér.")
        xd = str(valasz.content)
        if xd.lower() == "franciaország" and orszag == "Zaszlo1": await ctx.send("Eltaláltad! A helyes válasz Franciaország.")
        elif xd.lower() == "afganisztán" and orszag == "Zaszlo4": await ctx.send("Eltaláltad! A helyes válasz Afganisztán.")
        elif xd.lower() == "magyarország" or xd.lower() == "magyar" and orszag == "Zaszlo2": await ctx.send("Eltaláltad! A helyes válasz Magyarország.")
        elif xd.lower() == "albánia" and orszag == "Zaszlo3": await ctx.send("Eltaláltad! A helyes válasz Albánia.")
        elif xd.lower() == "afganisztán" and orszag == "Zaszlo9": await ctx.send("Eltaláltad! A helyes válasz Afganisztán.")
        elif xd.lower() == "algéria" and orszag == "Zaszlo5": await ctx.send("Eltaláltad! A helyes válasz Algéria.")
        elif xd.lower() in ("usa", "amerika", "amerikai egyesült államok") and orszag == "Zaszlo6": await ctx.send("Eltaláltad! A helyes válasz Amerikai Egyesült Államok.")
        elif xd.lower() == "andorra" and orszag == "Zaszlo7": await ctx.send("Eltaláltad! A helyes válasz Andorra.")
        elif xd.lower() == "angola" and orszag == "Zaszlo8": await ctx.send("Eltaláltad! A helyes válasz Angola.")
        elif xd.lower() == "argentína" and orszag == "Zaszlo9": await ctx.send("Eltaláltad! A helyes válasz Argentína.")
        elif xd.lower() == "ausztrália" and orszag == "Zaszlo10": await ctx.send("Eltaláltad! A helyes válasz Ausztrália.")
        elif xd.lower() == "bosznia" and orszag == "Zaszlo11": await ctx.send("Eltaláltad! A helyes válasz Bosznia.")
        elif xd.lower() == "ausztria" and orszag == "Zaszlo12": await ctx.send("Eltaláltad! A helyes válasz Ausztrália.")
        elif xd.lower() == "lengyelország" and orszag=="Zaszlo13": await ctx.send("Eltaláltad! A helyes válasz Lengyelország.")
        elif xd.lower() == "marokkó" and orszag=="Zaszlo14": await ctx.send("Eltaláltad! A helyes válasz Marokkó.")
        elif xd.lower() == "dél-korea" and orszag=="Zaszlo15": await ctx.send("Eltaláltad! A helyes válasz Dél-Korea.")
        elif xd.lower() == "japán" and orszag=="Zaszlo16": await ctx.send("Eltaláltad! A helyes válasz Japán.")
        elif xd.lower() == "dánia" and orszag=="Zaszlo18": await ctx.send("Eltaláltad! A helyes válasz Dánia.")
        elif xd.lower() == "kolumbia" and orszag=="Zaszlo19": await ctx.send("Eltaláltad! A helyes válasz Kolumbia.")
        elif xd.lower() == "bahrein" and orszag=="Zaszlo20": await ctx.send("Eltaláltad! A helyes válasz Bahrein.")
        elif xd.lower() == "bulgária" and orszag=="Zaszlo21": await ctx.send("Eltaláltad! A helyes válasz Bulgária.")
        else:
            if orszag == "Zaszlo1": await ctx.send("A válasz helytelen! A helyes válasz Franciaország volt.")
            elif orszag == "Zaszlo2": await ctx.send("A válasz helytelen! A helyes válasz Magyarország volt.")
            elif orszag == "Zaszlo3": await ctx.send("A válasz helytelen! A helyes válasz Albánia volt.")
            elif orszag == "Zaszlo4": await ctx.send("A válasz helytelen! A helyes válasz Afganisztán volt.")
            elif orszag == "Zaszlo5": await ctx.send("A válasz helytelen! A helyes válasz Algéria volt.")
            elif orszag == "Zaszlo6": await ctx.send("A válasz helytelen! A helyes válasz az Amerikai Egyesült Államok volt.")
            elif orszag == "Zaszlo7": await ctx.send("A válasz helytelen! A helyes válasz Andorra volt.")
            elif orszag == "Zaszlo8": await ctx.send("A válasz helytelen! A helyes válasz Angola volt.")
            elif orszag == "Zaszlo9": await ctx.send("A válasz helytelen! A helyes válasz Argentína volt.")
            elif orszag == "Zaszlo10": await ctx.send("A válasz helytelen! A helyes válasz Ausztrália volt.")
            elif orszag == "Zaszlo11": await ctx.send("A válasz helytelen! A helyes válasz Bosznia volt.")
            elif orszag == "Zaszlo12": await ctx.send("A válasz helytelen! A helyes válasz Ausztria volt.")
            elif orszag == "Zaszlo13": await ctx.send("A válasz helytelen! A helyes válasz Lengyelország volt.")
            elif orszag == "Zaszlo14": await ctx.send("A válasz helytelen! A helyes válasz Marokkó volt.")
            elif orszag == "Zaszlo15": await ctx.send("A válasz helytelen! A helyes válasz Dél-Korea volt.")
            elif orszag == "Zaszlo16": await ctx.send("A válasz helytelen! A helyes válasz Japán volt.")
            elif orszag == "Zaszlo18": await ctx.send("A válasz helytelen! A helyes válasz Dánia volt.")
            elif orszag == "Zaszlo19": await ctx.send("A válasz helytelen! A helyes válasz Kolumbia volt.")
            elif orszag == "Zaszlo20": await ctx.send("A válasz helytelen! A helyes válasz Bahrein volt.")
            elif orszag == "Zaszlo21": await ctx.send("A válasz helytelen! A helyes válasz Bulgária volt.")

    @commands.command(aliases=["dobokocka", "kocka"])
    async def dice(self, ctx):
        kocka = random.randint(1, 6)
        if kocka == 1:
            embed = discord.Embed(description=":black_circle::black_circle:\n:black_circle::white_circle:\n:black_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Dobókocka ({kocka})", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Dobókocka", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 2:
            embed = discord.Embed(description=":black_circle::black_circle:\n:white_circle::white_circle:\n:black_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Dobókocka ({kocka})", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Dobókocka", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 3:
            embed = discord.Embed(description=":white_circle::black_circle:\n:white_circle::black_circle:\n:white_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Dobókocka ({kocka})", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Dobókocka", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 4:
            embed = discord.Embed(description=":white_circle::white_circle:\n:white_circle::white_circle:\n:black_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Dobókocka ({kocka})", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Dobókocka", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 5:
            embed = discord.Embed(description=":white_circle::white_circle:\n:white_circle::white_circle:\n:white_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Dobókocka ({kocka})", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Dobókocka", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 6:
            embed = discord.Embed(description=":white_circle::white_circle:\n:white_circle::white_circle:\n:white_circle::white_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Dobókocka ({kocka})", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Dobókocka", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",ascii [szöveg]", aliases=["asciiart"])
    async def ascii(self, ctx, *, message):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.radonbot.hu/ascii?text={message}") as s:
                asd = await s.text()
                embed = f"```{asd.replace('<pre>', '').replace('</pre>', '')}```"
                await ctx.reply(embed, mention_author=False)

    @commands.command(usage=",mcszerver [szerver IP]")
    async def mcszerver(self, ctx, szerver):
        r = requests.get(f"https://api.mcsrvstat.us/2/{szerver}")
        resp = r.json()
        embed = discord.Embed(color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Játékosok", value=f"{resp['players']['online']}/{resp['players']['max']}")
        embed.add_field(name="MOTD", value=str(resp["motd"]["clean"]).replace("['", "").replace(",", "\n").replace("'", "").replace("'", "").replace("]", ""))
        embed.add_field(name="Verzió", value=resp["version"])
        embed.set_author(name=f"{szerver} :link:", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Dobókocka", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def ido(self, ctx):
        embed = discord.Embed(description=f"A jelenlegi idő: **{datetime.datetime.utcnow()}**!")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def kiló(self, ctx, member=None):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        age = random.randint(0, 160)
        if member == None:
            embed = discord.Embed(description=f"A te súlyod: **{age}** kg", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Kiló × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(title="Súly mérő", description=f"{member} súlya: **{age}** kg", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Kiló × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["kiusselek", "kiuselek", "kiüselek"], usage=[",kiüsselek [@említés]"])
    async def kiüsselek(self, ctx, member=None):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        embed = discord.Embed(title="Kiüsselek?", description=f"{ctx.author} brutálisan megfenyegette **{member}** felhasználót azzal, hogy kiüti! ÚÚÚÚÚÚÉNEZTNEMHAGYNÁM", color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"Kiüsselek? × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
        embed.set_image(url='https://images-ext-1.discordapp.net/external/UGJU907KkE5ptQpy8IiZ4oE1Os_5Q0jRoZR5E1GtJUU/%3Fcid%3D73b8f7b1151a82f551423406cb4f61f0211aa1338dc9c74f%26rid%3Dgiphy.mp4%26ct%3Dg/https/media1.giphy.com/media/l1J3G5lf06vi58EIE/giphy.mp4')
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",fight [@felhasználó]", aliases=["harc", "csata"])
    async def fight(self, ctx, member):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        harc = [f"{ctx.message.author}", f"{member.name}#{member.discriminator}"]
        uzenet = await ctx.reply(content=f"A verekedés elkezdődött **{ctx.message.author}** és **{member}** között! Hajrá!", mention_author=False)
        await asyncio.sleep(6)
        await uzenet.edit(content=f"**{random.choice(harc)}** Kiütötte az ellenfelét... (uhh) ")
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**{member}** elájult mert **{ctx.message.author}** kiütötte (szegény :( )")
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**__Az első kör véget ért!__ (GG)**")
        await asyncio.sleep(7)
        await uzenet.edit(content=f"**{random.choice(harc)}** lefejelte a falat! (Ouch)")
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**__A második kör is véget ért!__**")
        await asyncio.sleep(5)
        embed = discord.Embed(description=f"A harcot megnyerte: **{random.choice(harc)}**. Gratulálok!", color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Harc", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Harc", icon_url=self.client.user.avatar_url)
        await uzenet.edit(content=None, embed=embed)

    @commands.command(usage=",futóverseny [@felhasználó]", aliases=["run", "running", "fut", "futás", "futas", "futoverseny"])
    async def futóverseny(self, ctx, member):
        try: user = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        futás = [f"{ctx.message.author}", f"{user.name}#{user.discriminator}"]
        uzenet = await ctx.reply(content=f"A futóverseny elkezdődött!", mention_author=False)
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**{random.choice(futás)}** elfáradt... ")
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**{random.choice(futás)}** messze lehagyta ellenfelét!")
        await uzenet.edit(content=f"**{random.choice(futás)}** előre tört! ")
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**{random.choice(futás)}** kifulladt...")
        await asyncio.sleep(5)
        await uzenet.edit(content=f"**{user}** siet...")
        await asyncio.sleep(6)
        await uzenet.edit(content=f"Nagyon szoros a futam a két futó közt!")
        await asyncio.sleep(8)
        embed = discord.Embed(description=f"A futóversenyt megnyerte: **{random.choice(futás)}**. Gratulálok!", color=0xe9b603)
        embed.set_author(name="Futóverseny", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Futóverseny", icon_url=self.client.user.avatar_url)
        await uzenet.edit(content=None, embed=embed)

    @commands.command(usage=",swim [@felhasználó]")
    async def swim(self, ctx, member):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        futás = [ctx.author.name, member.name]
        uzenet = await ctx.reply(content=f"Az úszóverseny elkezdődött **{ctx.message.author}** és **{member}** között!", mention_author=False)
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**{random.choice(futás)}** átvette a vezetést... ")
        await asyncio.sleep(8)
        await uzenet.edit(content=f"**{random.choice(futás)}** elfáradt... ")
        await asyncio.sleep(8)
        await uzenet.edit(content=f"Az első kör véget ért!")
        await asyncio.sleep(5)
        await uzenet.edit(content=f"**{member}** előre tört!")
        await asyncio.sleep(6)
        await uzenet.edit(content=f"Nagyon szoros a verseny a két úszó között!")
        await asyncio.sleep(8)
        embed = discord.Embed(description=f"Az úszóversenyt megnyerte: **{random.choice(futás)}**. Gratulálok!", color=0xe9b603)
        embed.set_author(name="Úszóverseny", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Úszóverseny", icon_url=self.client.user.avatar_url)
        await uzenet.edit(content=None, embed=embed)

    @commands.command(aliases=["flip", "coin", "érmedobás", "cf", "érmefeldobás", "érme", "erme", "ermedobas", "ermefeldobas"])
    async def coinflip(self, ctx):
        coin = ['Fej','Írás']
        embed = discord.Embed(description= f'**Eredmény:** {random.choice(coin)}!', color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Coinflip", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Coinflip", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",meleg [@felhasználó]", aliases=["howpride", "gayometer", "kimaanyja"])
    async def howgay(self, ctx, member=None):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        gays = random.randint(0, 100)
        if member == None:
            embed = discord.Embed(description=f"{ctx.author.mention} {gays}%-ban meleg!", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Melegségi teszt × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"{member.mention} {gays}%-ban meleg!", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Melegségi teszt × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",pofon [@felhasználó]", aliases=["slap", "megpofoz", "felpofoz"])
    async def pofon(self, ctx, member):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        embed = discord.Embed(description=f"**Megpofoztad {member}-t**", color=0xe9b603)
        embed.set_image(url="https://images-ext-1.discordapp.net/external/i0PYbQd9TEUFAIlIWSZNdW9UXQi-tMcoP2TtJ2Q9Y4U/https/i.gifer.com/XaaW.gif")
        embed.set_author(name=f"Pofon × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",kill <felhasználó> (utolsó szó)", aliases=["megöl", "gyilkol", "death", "megol", "ol", "öl", "ölés", "oles"])
    async def kill(self, ctx, member, *, message1=None):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        szabadlab = ['Igen', 'Nem']
        helyek = ['Az áldozat házába','A pincében','Az erdőben','Egy sikátorban','Egy buliban']
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0xe9b603)
        embed.add_field(name="Gyilkos", value=ctx.message.author)
        embed.add_field(name="Gyilkos szabadlábon?", value=f"{random.choice(szabadlab)}")
        embed.add_field(name="Áldozat", value=f"{member}")
        embed.add_field(name="Gyilkosság helye", value=f"{random.choice(helyek)}")
        if message1 == None: pass
        else: embed.add_field(name="Utolsó szava", value=f",,{message1}''")
        if member.id == ctx.author.id: embed.set_author(name=f"Öngyilkosság", icon_url=ctx.author.avatar_url)
        else: embed.set_author(name=f"Gyilkosság", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Gyilkosság", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["jóslat", "jós", "jos", "joslat"])
    async def jóslás(self, ctx):
        joslatok = ['Lesz egy kiskutyád', 'Nagy házad lesz', 'Kapsz egy Porschet', 'Súlyos baleseted lesz', 'Elmész Görögországba nyaralni', 'Lesz egy Olasz éttermed', 'Kézilabda edző leszel', 'Felvesznek álmaid iskolájába', 'Sikeres életed lesz', 'Rövid életed lesz', 'Autóbaleseted lesz', 'Hosszú életed lesz', 'Befolyásos ember leszel', 'Hamarosan megtalálod az igazit', 'Az egyik családtagodra rossz jövő vár', 'Megkapod a jobb jegyet az iskolában', 'Gazdag leszel', 'A gyerekeid egészségesek lesznek', 'Életed során kevés választási lehetőséget fogsz kapni']
        josnok = ['Éva', 'Mari', 'Andrea', 'Bözsi', 'Jázmin', 'Alma', 'Kriszta', 'Rebeka', 'Vivien', 'Irma']
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0xe9b603)
        embed.set_author(name="Jóslás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Jóslás", icon_url=self.client.user.avatar_url)
        embed.add_field(name="Jóslat", value=f"{random.choice(joslatok)}")
        embed.add_field(name='Jósnő',value=f"{random.choice(josnok)}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/FostTalicska/new.json?sort=hot') as r:
                    res = await r.json()
                    embed = discord.Embed(color=0xe9b603, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"{ctx.author.name} × Meme", icon_url=self.client.user.avatar_url)
                    embed.set_author(text="Megnyitáshoz katt ide!", url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                    embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                    await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def vár(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/castles/new.json?sort=hot') as r:
                    res = await r.json()
                    embed = discord.Embed(description=f"Megnyitáshoz [katt ide]({res['data']['children'][random.randint(0, 25)]['data']['url']})", color=0xe9b603, timestamp=datetime.datetime.utcnow()) 
                    embed.set_author(name="Várak", icon_url=ctx.author.avatar_url)
                    embed.set_footer(text=f"{ctx.author.name} × Várak", icon_url=self.client.user.avatar_url)
                    embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                    await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["játék", "games", "ajánlottjáték", "jatek"])
    async def game(self, ctx):
        joslatok = ['`Roblox`','`Battlefront`','`Minecraft`','`Apex Legends`','`Fortnite`','`FIFA 19`','`Call of Duty`','`Rocket League`','`Among Us`','`Crossout`','`League of Legends`','`Sea of Thieves`','`GTA V`','`CS:GO`','`PUBG`']
        embed = discord.Embed(title="Ajánlott játék", timestamp=datetime.datetime.utcnow(), color=0xe9b603)
        embed.add_field(name="Neked ajánlott játék:", value=f"{random.choice(joslatok)}")
        embed.set_author(name="Ajánlás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Ajánlás", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",mcskin [minecraft felhasználónév]")
    async def mcskin(self, ctx, username):
        embed = discord.Embed(description=f"[Katt ide](https://minotar.net/armor/body/{username}/100.png)", color=0xe9b603)
        embed.set_image(url=f"https://minotar.net/armor/body/{username}/100.png")
        embed.set_author(name="Skin", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Skin", icon_url=self.client.user.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["kpo"], usage=",rps [kő/papír/olló]")
    async def rps(self, ctx, valasztas):
        rpswords = [ ":rock: Kő", ":newspaper: Papír", ":scissors: Olló"]
        embed = discord.Embed(color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Kő-papír-olló", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Kő-papír-olló", icon_url=self.client.user.avatar_url)
        if valasztas == "kő":
            embed.add_field(name="A te választásod", value=":rock: Kő", inline=True)
            embed.add_field(name="A bot választása", value=random.choice(rpswords), inline=True)
        elif valasztas == "papír":
            embed.add_field(name="A te választásod", value=":newspaper: Papír", inline=True)
            embed.add_field(name="A bot választása", value=random.choice(rpswords), inline=True)
        elif valasztas == "olló":
            embed.add_field(name="A te választásod", value=":scissors:: Olló", inline=True)
            embed.add_field(name="A bot választása", value=random.choice(rpswords), inline=True)
        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Fun(client))

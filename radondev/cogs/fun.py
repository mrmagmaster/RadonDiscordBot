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

    @commands.command(usage=",love [1. felhasználó] [2. felhasználó]")
    async def love(self, ctx, member1, member2):
        try: member1 = await commands.MemberConverter().convert(ctx, member1); member2 = await commands.MemberConverter().convert(ctx, member2)
        except: 
            embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Radon × Hiba", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
            return
        if member1 == member2: await ctx.reply("Aww, nyilván 100%, szeresd magad :)", mention_author=False);return
        embed = discord.Embed(description=f"{member1.mention} :grey_question: {member2.mention} [SZÁMOLÁS...]", color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Szeretet", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{member1.name} - {member2.name} × Kérte: {ctx.author.name}", icon_url=self.client.user.avatar_url)
        msg = await ctx.reply(embed=embed, mention_author=False)
        szam = random.randint(0, 100)
        if szam >= 90: emoji=":heart_on_fire:"
        if szam >=70 and szam< 90: emoji=":revolving_hearts:"
        if szam >=50 and szam<70: emoji=":heart:"
        if szam >=30 and szam<50: emoji=":broken_heart:"
        if szam >=0 and szam<30: emoji=":mending_heart:"
        await asyncio.sleep(random.randint(1, 4))
        embed = discord.Embed(description=f"{member1.mention} {emoji} {member2.mention} [**{szam}%**]")
        embed.set_author(name="Szeretet", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{member1.name} - {member2.name} × Kérte: {ctx.author.name}", icon_url=self.client.user.avatar_url)
        await msg.edit(embed=embed, content=None)

    @commands.command(usage=",iq (@felhasználó)")
    async def iq(self, ctx, member=None):
        if member == None:
            embed = discord.Embed(  title="IQ",
                                    description=f"{ctx.author.mention} IQ-ja: **{random.randint(60, 230)}** IQ pont. Büszkék vagyunk rád.",
                                    color=0xe9b703,
                                    timestamp=datetime.datetime.utcnow())
            embed.set_footer(text="Radon × IQ", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            try:
                member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Radon × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed)
                return
            embed = discord.Embed(title="IQ", description=f"{member.mention} IQ-ja: **{random.randint(60, 170)}** IQ pont. Büszkék vagyunk rád.", color=0xe9b703, timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)


#    @commands.command()
#    async def amőba(self, ctx):
#        board = ["  ", "1", "2", "3", "1 ", "-", "-", "-", "2 ", "-", "-", "-", "3 ", "-", "-", "-"]
#        have_winner = False
#        player_one_turn = True
#
#        while not have_winner:
#            # Kirajzolni a játékteret:
#            for i in range(0, 16, 4): ctx.send(```board[i] + "|" + board[i+1] + "|" + board[i+2] + "|" + board[i+3] + "|"```)
#            if player_one_turn: ctx.send("Az 1. játékos következik!")
#            else: ctx.send("A 2. játékos következik!")
#            new_place = False
#            while not new_place: 
#                row = col = 10
#                while row > 3 or row < 1: row = int(input("Melyik oszlopba szeretnél tenni? "))
#                while col > 3 or col < 1: col = int(input("Melyik sorba szeretnél tenni? "))
#                if board[4 * row + col] == "-": new_place = True
#            if player_one_turn: board[4 * row + col] = "X"
#            else: board[4*row+col] = "O"
#            # Nyertesek megnézése:
#            #Vízszintes:
#            if board[5] == board[6] and board[5] == board[7] and board[6] == board[7] and board[5] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#                have_winner = True
#            if board[9] == board[10] and board[9] == board[11] and board[10] == board[11] and board[9] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#                have_winner = True
#            if board[13] == board[14] and board[13] == board[15] and board[14] == board[15] and board[13] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#                have_winner = True
#            #Függőleges:
#            if board[5] == board[9] and board[5] == board[13] and board[9] == board[13] and board[5] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#                have_winner = True
#            if board[6] == board[10] and board[6] == board[14] and board[10] == board[14] and board[6] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#                have_winner = True
#            if board[7] == board[11] and board[7] == board[15] and board[11] == board[15] and board[7] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#            #Átlós:
#            if board[13] == board[6] and board[13] == board[7] and board[6] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#                have_winner = True
#            if board[5] == board[10] and board[5] == board[15] and board[5] != "-":
#                if player_one_turn: ctx.send("Nyert az 1. játékos!")
#                else: ctx.send("Nyert a 2. játékos!")
#                have_winner = True
#
#            #Döntetlen:
#            if not have_winner and "-" not in board:
#                have_winner = True
#                ctx.send("Nincs győztes!")
#            if player_one_turn: player_one_turn = False
#            else: player_one_turn = True
#
#        for i in range(0, 16, 4): ctx.send(```board[i] + "|" + board[i+1] + "|" + board[i+2] + "|" + board[i+3] + "|"```)

    @commands.command()
    async def fortnájt(self, ctx):
        msg = await ctx.reply(content="https://youtu.be/QqRLVFRe9AU", mention_author=False)
        await msg.add_reaction("🤣")

    @commands.command()
    async def danbox(self, ctx):
        embed = discord.Embed(description=f"A DanBox letöltéséhez [kattints ide](http://danbox.radonbot.hu)!", color=0xe9b703, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="DanBox")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",segberúg [@említés]")
    async def segberúg(self, ctx, member: discord.Member):
        if member == ctx.author:
            await ctx.reply(content="Hé, hé, azé má na, tudom hogy különleges vagy, de annyira csak nem, hogy seggberúgd magad xd", mention_author=False)
            return
        if member.mention == self.client.user.mention:
            await ctx.reply(content="WOAH WOAH WOAH *kitér a seggberúgás elől* te engem te ne!", mention_author=False)
            return
        if member.id in (648168353453572117, 654721418273226793, 609764483229024297, 796769651555958784, 418024746253287425, 696764877967982722, 758017934449836082, 727510249338175529, 406137394228625419, 693076081992925234, 751133665492336791):
            await ctx.reply(content="no\nstop\npliz\nminket ne\nkegyelmezz", mention_author=False)
            return
        #gifs = [ "https://tenor.com/view/cat-duckling-kicked-gif-14427214", "https://tenor.com/view/looney-tunes-elmer-bugs-bunny-bugs-kick-gif-16789937", "https://tenor.com/view/bette-midler-danny-devito-ex-husband-husband-ruthless-people-gif-14617447", "https://tenor.com/view/kick-in-the-butt-fly-away-kick-gif-15177856" ]
        embed = discord.Embed(title="Seggberúgás", description=f"{ctx.author.mention} halálosan megfenyegette {member.mention}-t egy seggberúgással!", color=0xe9b703, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text="Radon × Nosztalgia")
        #embed.set_image(url=random.choice(gifs))
        await ctx.reply(embed=embed, mention_author=False)


    @commands.command(aliases=["calculator", "matek", "maths"], usage=",calc [szám1] [művelet] [szám2]")
    async def calc(self, ctx, arg1: int, arg2, arg3: int):
        if arg1 > 5000000 or arg3 > 5000000:
            await ctx.reply(content="Nem lehet ennyi számot beírni!", mention_author=False)
            return
        if arg1 > 100 or arg3 > 100 and arg2 == "^":
            await ctx.reply(content="Nem lehet ennyi számot beírni!", mention_author=False)
            return
        if arg2 == "+":
            valasz = arg1 + arg3
        if arg2 == "-":
            valasz = arg1 - arg3
        if arg2 in ("*", "×", "."):
            valasz = arg1 * arg3
        if arg2 in ("/", "÷", ":"):
            valasz = arg1 / arg3
        if arg2 == "^":
            valasz = arg1 ** arg3
        await ctx.reply(content=f"Az eredmény: **{valasz}**!", mention_author=False)

    @commands.command(usage=",randomszám [szám1] [szám2]")
    async def randomszám(self, ctx, szam1: int, szam2: int):
        vegsoszam = random.randint(szam1, szam2)
        await ctx.reply(content=f"A random szám: **{vegsoszam}**!", mention_author=False)

    @commands.command(usage=",age (@felhasználó)",aliases=["kor", "életkor", "eletkor"])
    async def age(self, ctx, member=None):
        age = random.randint(1, 100)
        if member == None:
            embed = discord.Embed(description=f"A te életkorod: {age} év", color=0xe9b703, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Kor × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(title="Életkor mérő", description=f"{member} kora: {age} év", color=0xe9b703, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Kor × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
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
        if member == None:
            embed = discord.Embed(description=f"E-Péniszed hossza: {random.choice(dicks)}", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Méret × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            try:
                member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xe9b603, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            embed = discord.Embed(description=f"{member.mention} e-pénisze: {random.choice(dicks)}", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text="Nem tudom miért csinálom ezt × Radon")
            embed.set_author(name=f"Méret × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",cici (@felhasználó)",aliases=["mell", "csöcs", "domborzat", "uncode", "uc"])
    async def cici(self, ctx, member=None):
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
            embed.set_author(name=f"Méret × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:
            try:
                member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xe9b603, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Radon × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            embed = discord.Embed(description=f"E-Csöcsöd mérete: {member.mention}-nak/nek: {random.choice(dicks)}", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Méret × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",magasság [@felhasználó]",aliases=["magassag", "height", "mag", "cm"])
    async def magasság(self, ctx, member : discord.Member):
        embed = discord.Embed(title="Magasság", description=f"{member.mention} magassága: `{random.randint(150, 205)}`cm", color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text="Magasság", icon_url=member.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["zászló"])
    async def zaszlo(self, ctx):
        path = ["Zaszlo1", "Zaszlo2", "Zaszlo3", "Zaszlo4", "Zaszlo5", "Zaszlo6", "Zaszlo7", "Zaszlo8", "Zaszlo9", "Zaszlo10"]
        orszag = random.choice(path)
        await ctx.reply(content="A játék elindult. 2 perced lesz válaszolni, a választ prefix __nélkül__ a chatbe írdd. Az ország a következő:", file=discord.File(f'./zaszlok/{orszag}.png'), mention_author=False)
        def check(message): return message.channel == ctx.channel and message.author == ctx.author and message.guild == ctx.guild
        try: valasz = await self.client.wait_for('message', check=check, timeout=120)
        except asyncio.TimeoutError: await ctx.send("Nem válaszoltál időben! A játék véget ér.")
        xd = str(valasz.content)
        if xd.lower() == "franciaország" and orszag == "Zaszlo1": await ctx.send("Eltaláltad! A helyes válasz Franciaország.")
        elif xd.lower() == "afganisztán" and orszag == "Zaszlo4": await ctx.send("Eltaláltad! A helyes válasz Afganisztán.")
        elif xd.lower() == "magyarország" or xd.lower() == "magyar" and orszag == "Zaszlo2": await ctx.send("Eltaláltad! A helyes válasz Magyarország.")
        elif xd.lower() == "albánia" and orszag == "Zaszlo3": await ctx.send("Eltaláltad! A helyes válasz Albánia.")
        elif xd.lower() == "afganisztán" and orszag == "Zaszlo9": await ctx.send("Eltaláltad! A helyes válasz Afganisztán.")
        elif xd.lower() == "algéria" and orszag == "Zaszlo5": await ctx.send("Eltaláltad! A helyes válasz Algéria.")
        elif xd.lower() in ("usa", "amerika", "amerikai egyesült államok", "aeá", "united states of america") and orszag == "Zaszlo6": await ctx.send("Eltaláltad! A helyes válasz Amerikai Egyesült Államok.")
        elif xd.lower() == "andorra" and orszag == "Zaszlo7": await ctx.send("Eltaláltad! A helyes válasz Andorra.")
        elif xd.lower() == "angola" and orszag == "Zaszlo8": await ctx.send("Eltaláltad! A helyes válasz Angola.")
        elif xd.lower() == "argentína" and orszag == "Zaszlo9": await ctx.send("Eltaláltad! A helyes válasz Argentína.")
        elif xd.lower() == "ausztrália" and orszag == "Zaszlo10": await ctx.send("Eltaláltad! A helyes válasz Ausztrália.")
        elif xd.lower() == "bosznia" and orszag == "Zaszlo11": await ctx.send("Eltaláltad! A helyes válasz Bosznia.")
        elif xd.lower() == "ausztria" and orszag == "Zaszlo12": await ctx.send("Eltaláltad! A helyes válasz Ausztrália.")
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

    @commands.command(aliases=["dobokocka", "baszdfejbemagadat", "kocka"])
    async def dice(self, ctx):
        kocka = random.randint(1, 6)
        if kocka == 1:
            embed = discord.Embed(title=f"🎲 Dobókocka ({kocka})", description=":black_circle::black_circle:\n:black_circle::white_circle:\n:black_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Radon × Dobókocka", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 2:
            embed = discord.Embed(title=f"🎲 Dobókocka ({kocka})", description=":black_circle::black_circle:\n:white_circle::white_circle:\n:black_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Radon × Dobókocka", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 3:
            embed = discord.Embed(title=f"🎲 Dobókocka ({kocka})", description=":white_circle::black_circle:\n:white_circle::black_circle:\n:white_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Radon × Dobókocka", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 4:
            embed = discord.Embed(title=f"🎲 Dobókocka ({kocka})", description=":white_circle::white_circle:\n:white_circle::white_circle:\n:black_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Radon × Dobókocka", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 5:
            embed = discord.Embed(title=f"🎲 Dobókocka ({kocka})", description=":white_circle::white_circle:\n:white_circle::white_circle:\n:white_circle::black_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Radon × Dobókocka", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        if kocka == 6:
            embed = discord.Embed(title=f"🎲 Dobókocka ({kocka})", description=":white_circle::white_circle:\n:white_circle::white_circle:\n:white_circle::white_circle:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"Radon × Dobókocka", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",ascii [szöveg]", aliases=["asciiart"])
    async def ascii(self, ctx, *, message):
        message = urllib.parse.quote_plus(message)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.radonbot.hu/ascii?text={message}") as s:
                asd = await s.text()
                embed = f"```{asd.replace('<pre>', '').replace('</pre>', '')}```"
                await ctx.reply(embed, mention_author=False)

    @commands.command(usage=",mcszerver [szerver IP]")
    async def mcszerver(self, ctx, szerver):
        r = requests.get(f"https://api.mcsrvstat.us/2/{szerver}")
        resp = r.json()
        embed = discord.Embed(title=f"{szerver} :link:", color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Játékosok", value=f"{resp['players']['online']}/{resp['players']['max']}")
        embed.add_field(name="MOTD", value=str(resp["motd"]["clean"]).replace("['", "").replace(",", "\n").replace("'", "").replace("'", "").replace("]", ""))
        embed.add_field(name="Verzió", value=resp["version"])
        await ctx.reply(embed=embed, mention_author=False)

#    @commands.command(usage=[",binary [szám]"], aliases=["bináris"])
#    async def binary(self, ctx, content):
#        szam = bin(content)
#        embed=discord.Embed(title="Bináris kód", description="A szám bináris kódban: " + szam, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
#        await ctx.reply(embed=embed)

    @commands.command(usage=[",kozososzto [első szám] [második szám]"], aliases=["kozos_oszto", "közösosztó", "közös_osztó", "lko"])
    async def kozososzto(self, ctx, szam1: int, szam2: int):
        if szam1 > 5000 or szam2 > 5000: 
            return
        try:
            for i in range(1,szam1):
                if szam1 % i == 0 and szam2 % i == 0:
                    lko = i
            await ctx.reply(content=f"A(z) {szam1} és a(z) {szam2} közös osztója: {lko}", mention_author=False)
        except:
            await ctx.reply(content="Nem található közös osztó.", mention_author=False)

    @commands.command()
    async def ido(self, ctx):
        embed = discord.Embed(description=f"A jelenlegi idő: **{datetime.datetime.utcnow()}**!")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def bc(self, ctx):
        r = requests.get(f"https://api.mcsrvstat.us/2/play.birodalomcraft.hu")
        resp = r.json()
        embed = discord.Embed(title=f"BirodalomCraft Szerver információjai <:birodalomcraft:775045871737634856>", color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Játékosok", value=f"{resp['players']['online']}/{resp['players']['max']}")
        embed.add_field(name="MOTD", value=str(resp["motd"]["clean"]).replace("['", "").replace(",", "\n").replace("'", "").replace("'", "").replace("]", ""))
        embed.add_field(name="Verzió", value=resp["version"])
        embed.set_thumbnail(url="https://images-ext-2.discordapp.net/external/Nrmj1iOyLE5riI1QqqVxma41eyjSqWqZof9z2ehWxdg/https/media.discordapp.net/attachments/675056349196845096/825812713917644800/bc2_eredeti.png")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def kiló(self, ctx, member=None):
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
        if member == None:
            await ctx.reply("Kérlek említs meg egy felhasználót")
        else:
            embed = discord.Embed(title="Kiüsselek?", description=f"{ctx.author} brutálisan megfenyegette **{member}** felhasználót azzal, hogy kiüti! ÚÚÚÚÚÚÉNEZTNEMHAGYNÁM", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Kiüsselek? × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            embed.set_image(url='https://images-ext-1.discordapp.net/external/UGJU907KkE5ptQpy8IiZ4oE1Os_5Q0jRoZR5E1GtJUU/%3Fcid%3D73b8f7b1151a82f551423406cb4f61f0211aa1338dc9c74f%26rid%3Dgiphy.mp4%26ct%3Dg/https/media1.giphy.com/media/l1J3G5lf06vi58EIE/giphy.mp4')
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",fight <@felhasználó/id>", aliases=["harc", "csata"])
    async def fight(self, ctx, member):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except: 
            embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xe9b603, timestamp=datetime.datetime.utcnow())
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
        embed.set_author(name=f"Harc × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await uzenet.edit(content=None, embed=embed)

    @commands.command(usage=",futóverseny <@felhasználó/id>", aliases=["run", "running", "fut", "futás", "futas", "futoverseny"])
    async def futóverseny(self, ctx, user):
        try: user = await commands.MemberConverter().convert(ctx, user)
        except: 
            embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xe9b603, timestamp=datetime.datetime.utcnow())
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
        await uzenet.edit(content=f"**{user}** ")
        await asyncio.sleep(6)
        await uzenet.edit(content=f"Nagyon szoros a futam a két futó közt!")
        await asyncio.sleep(8)
        embed = discord.Embed(description=f"A futóversenyt megnyerte: **{random.choice(futás)}**. Gratulálok!", color=0xe9b603)
        embed.set_author(name=f"Futóverseny × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await uzenet.edit(content=None, embed=embed)

    @commands.command(usage=",swim [@felhasználó]")
    async def swim(self, ctx, member: discord.Member):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except: 
            embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xFF9900, timestamp=datetime.datetime.utcnow())
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
        await uzenet.edit(content=f"Nagyon szoros a verseny a két futó között!")
        await asyncio.sleep(8)
        embed = discord.Embed(description=f"A futóversenyt megnyerte: **{random.choice(futás)}**. Gratulálok!", color=0xe9b603)
        embed.set_author(name=f"Úszóverseny × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await uzenet.edit(content=None, embed=embed)

    @commands.command(aliases=["flip", "coin", "érmedobás", "cf", "érmefeldobás", "érme", "erme", "ermedobas", "ermefeldobas"])
    async def coinflip(self, ctx):
        coin = ['Fej','Írás']
        embed = discord.Embed(title="A pénzt feldobtam!", description= f'**Eredmény:** {random.choice(coin)}!', color=0xe9b603, timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=f"Coinflip  × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",meleg [@felhasználó]", aliases=["howmeleg", "pride"])
    async def howgay(self, ctx, member: discord.Member=None):
        gays = random.randint(0, 100)
        if member == None:
            embed = discord.Embed(description=f"{ctx.author.mention} {gays}%-ban meleg!", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Melegségi teszt × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
        else:

            embed = discord.Embed(description=f"{member.mention} {gays}%-ban meleg!", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.set_author(name=f"Melegségi teszt × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.message.author.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",pofon <felhasználó>", aliases=["slap", "megpofoz", "felpofoz"])
    async def pofon(self, ctx, member):
        try: member = await commands.MemberConverter().convert(ctx, member)
        except: 
            embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xFF9900, timestamp=datetime.datetime.utcnow())
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
            embed = discord.Embed(description="Nem található ilyen felhasználó! <:radon_x:811191514482212874>", color=0xFF9900, timestamp=datetime.datetime.utcnow())
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
        if message1 == None:
            pass
        else:
            embed.add_field(name="Utolsó szava", value=f",,{message1}''")
        if member.id == ctx.author.id:
            embed.set_author(name=f"Öngyilkosság × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        else:
            embed.set_author(name=f"Gyilkosság × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["jóslat", "prediction", "predict", "pre", "jós", "jos", "joslat"])
    async def jóslás(self, ctx):
        joslatok = ['Gazdag leszel', 'Szegény leszel', 'Megtalálod az igazi szerelmet',
            'Macskákkal fogod leélni az életed','Felvesznek az álom munkahelyedre','Kirúgnak az állásodból',
            'Lesz két gyereked', 'Jól fogsz tanulni','Nem fogsz jól tanulni','Életed legjobb döntéseit fogod meghozni',
            'Életed legrosszabb döntéseit fogod meghozni','A családoddal sokáig fogtok boldogan élni','Lesz egy baleseted', 'Találkozni fogsz Varga Irénnel a nyugatiba',
            'Megfogod nyerni az ötös lottót', 'Híres leszel', 'Sok követőd lesz tiktokon',
            'A világ legjobb focistája leszel', 'A világ legjobb énekese leszel', 'Lesz 3 feleséged', 'Rengeteg követőd lesz PicNodeon',
            'Lesz 10 házad', 'Lesz sok követőd instagramon', 'Mindenki szeretni fog', 'Mindenki megutál']
        josnok = ['Marcsi', 'Magdi', 'Mari','Juliska', 'Anett', 'Irénke', 'Bözsi', 'Etelka', 'Jázmin', 'Sarolta']
        embed = discord.Embed(timestamp=datetime.datetime.utcnow(), color=0xe9b603)
        embed.set_author(name=f"Jóslás × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Jóslat", value=f"{random.choice(joslatok)}")
        embed.add_field(name='Jósnő',value=f"{random.choice(josnok)}")
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/FostTalicska/new.json?sort=hot') as r:
                    res = await r.json()
                    embed = discord.Embed(description=f"Megnyitáshoz [katt ide]({res['data']['children'][random.randint(0, 25)]['data']['url']})", color=0xe9b603, timestamp=datetime.datetime.utcnow()) 
                    embed.set_author(name=f"Meme × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)   
                    
                    embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                    await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["var16"])
    async def vár(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/castles/new.json?sort=hot') as r:
                    res = await r.json()
                    embed = discord.Embed(description=f"Megnyitáshoz [katt ide]({res['data']['children'][random.randint(0, 25)]['data']['url']})", color=0xe9b603, timestamp=datetime.datetime.utcnow()) 
                    embed.set_author(name=f"VAR16-ok × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)   
                    embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                    await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["játék", "games", "ajánlottjáték", "jatek"])
    async def game(self, ctx):
        joslatok = ['`Roblox`','`Battlefront`','`Minecraft`','`Apex Legends`','`Fortnite`','`FIFA 19`','`Call of Duty`','`Rocket League`','`Among Us`','`Crossout`','`League of Legends`','`Sea of Thieves`','`GTA V`','`CS:GO`','`PUBG`']
        embed = discord.Embed(title="Ajánlott játék", timestamp=datetime.datetime.utcnow(), color=0xe9b603)
        embed.add_field(name="Neked ajánlott játék:", value=f"{random.choice(joslatok)}")
        embed.set_footer(text="Radon × Játékajánlás", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",mcskin [minecraft felhasználónév]")
    async def mcskin(self, ctx, username):
        embed = discord.Embed(description=f"[Katt ide](https://minotar.net/armor/body/{username}/100.png)", color=0xe9b603)
        embed.set_image(url=f"https://minotar.net/armor/body/{username}/100.png")
        embed.set_footer(text="Radon × Minecraft skin", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["kpo"], usage=",rps [kő/papír/olló]")
    async def rps(self, ctx, valasztas):
        rpswords = [ ":rock: Kő", ":newspaper: Papír", ":scissors: Olló"]
        if valasztas == "kő":
            embed = discord.Embed(title="Kő-papír-olló", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="A te választásod", value=":rock: Kő", inline=True)
            embed.add_field(name="A bot választása", value=random.choice(rpswords), inline=True)
        elif valasztas == "papír":
            embed = discord.Embed(title="Kő-papír-olló", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="A te választásod", value=":newspaper: Papír", inline=True)
            embed.add_field(name="A bot választása", value=random.choice(rpswords), inline=True)
        elif valasztas == "olló":
            embed = discord.Embed(title="Kő-papír-olló", color=0xe9b603, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="A te választásod", value=":scissors:: Olló", inline=True)
            embed.add_field(name="A bot választása", value=random.choice(rpswords), inline=True)
        else:
            embed = discord.Embed(title="Hé!", description="Választási lehetőségek: `kő`, `papír`, `olló`.\nFontos, hogy csak úgy írhatod le, ahogy ide le van írva!")
        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Fun(client))

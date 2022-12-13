import discord
from discord.ext import commands
import datetime
import asyncio
import random
from main import db

rarities = {
    "ÁTLAGOS": {
        "chance": 80,
        "value": 2,
        "name": "ÁTLAGOS"
    },
    "NEM ÁTLAGOS": {
        "chance": 70,
        "value": 3,
        "name": "NEM ÁTLAGOS"
    },
    "RITKA": {
        "chance": 50,
        "value": 5,
        "name": "RITKA"
    },
    "NAGYON RITKA": {
        "chance": 10,
        "value": 10,
        "name": "NAGYON RITKA"
    },
    "EPIKUS": {
        "chance": 5,
        "value": 20,
        "name": "EPIKUS"
    },
    "LEGENDÁS": {
        "chance": 2,
        "value": 50,
        "name": "LEGENDÁS"
    },
    "LEHETETLEN": {
        "chance": 0.1,
        "value": 100,
        "name": "LEHETETLEN"
    }
}

ftypes = {
    "PONTY": {
        "chance": 90,
        "value": 2,
        "name": "PONTY"
    },
    "LAZAC": {
        "chance": 80,
        "value": 3,
        "name": "LAZAC"
    },
    "KESZEG": {
        "chance": 70,
        "value": 4,
        "name": "KESZEG"
    },
    "HARCSA": {
        "chance": 60,
        "value": 5,
        "name": "HARCSA"
    },
    "KÁRÁSZ": {
        "chance": 50,
        "value": 6,
        "name": "KÁRÁSZ"
    },
    "KECSEGE": {
        "chance": 40,
        "value": 7,
        "name": "KECSEGE"
    },
    "CSUKA": {
        "chance": 50,
        "value": 6,
        "name": "CSUKA"
    },
    "PISZTRÁNG": {
        "chance": 30,
        "value": 8,
        "name": "PISZTRÁNG"
    },
    "ANGOLNA": {
        "chance": 80,
        "value": 3,
        "name": "ANGOLNA"
    },
    "SÜGÉR": {
        "chance": 60,
        "value": 5,
        "name": "SÜGÉR"
    },
    "TÖRPEHARCSA": {
        "chance": 70,
        "value": 4,
        "name": "TÖRPEHARCSA"
    },
    "HERING": {
        "chance": 50,
        "value": 6,
        "name": "HERING"
    },
    "INGOLA": {
        "chance": 10,
        "value": 10,
        "name": "INGOLA"
    }
}

atypes = {
    "BIRKA": {
        "chance": 90,
        "value": 2,
        "name": "BIRKA"
    },
    "FARKAS": {
        "chance": 30,
        "value": 3,
        "name": "FARKAS"
    },
    "NYÚL": {
        "chance": 90,
        "value": 1,
        "name": "NYÚL"
    },
    "ŐZ": {
        "chance": 70,
        "value": 5,
        "name": "ŐZ"
    },
    "SZARVAS": {
        "chance": 70,
        "value": 6,
        "name": "SZARVAS"
    },
    "VADDISZNÓ": {
        "chance": 80,
        "value": 4,
        "name": "VADDISZNÓ"
    },
    "FÁCÁN": {
        "chance": 50,
        "value": 5,
        "name": "FÁCÁN"
    },
    "MEDVE": {
        "chance": 60,
        "value": 8,
        "name": "MEDVE"
    },
    "RÓKA": {
        "chance": 30,
        "value": 5,
        "name": "RÓKA"
    },
}

oretypes = {
    "BRONZ": {
        "chance": 90,
        "value": 20,
        "name": "BRONZ"
    },
    "KVARC": {
        "chance": 80,
        "value": 30,
        "name": "KVARC"
    },
    "VAS": {
        "chance": 90,
        "value": 50,
        "name": "VAS"
    },
    "MÉSZKŐ": {
        "chance": 70,
        "value": 60,
        "name": "MÉSZKŐ"
    },
    "SZÉN": {
        "chance": 70,
        "value": 40,
        "name": "SZÉN"
    },
    "SÁRGARÉZ": {
        "chance": 60,
        "value": 50,
        "name": "SÁRGARÉZ"
    },
    "EZÜST": {
        "chance": 40,
        "value": 70,
        "name": "EZÜST"
    },
    "ARANY": {
        "chance": 20,
        "value": 100,
        "name": "MÉSZKŐ"
    },
    "GYÉMÁNT": {
        "chance": 5,
        "value": 300,
        "name": "MÉSZKŐ"
    },
    
    "SMARAGD": {
        "chance": 2,
        "value": 400,
        "name": "SMARAGD"
    },
    "RUBINT": {
        "chance": 0.5,
        "value": 1000,
        "name": "RUBINT"
    },
    "ALUMÍNIUM": {
        "chance": 70,
        "value": 40,
        "name": "ALUMÍNIUM"
    },
    "BAUXIT": {
        "chance": 60,
        "value": 50,
        "name": "BAUXIT"
    },
    "URÁN": {
        "chance": 0.5,
        "value": 1000,
        "name": "URÁNÉRC"
    },
    "ÓLOM": {
        "chance": 80,
        "value": 60,
        "name": "MÉSZKŐ"
    },
    "MANGÁN": {
        "chance": 30,
        "value": 80,
        "name": "MÉSZKŐ"
    },
}

def fish(ftype: int, size: int, rarity: int):
    x = ftype
    y = size
    z = rarity
    return z*(x+y)

def hunt(atype: int, weight: int, rarity: int):
    x = atype
    y = weight
    z = rarity
    return (z*(x+y))*5

def mine(ore: int, weight: int, rarity: int):
    x = ore
    y = weight
    z = rarity
    return ((x*y)*5*z)*3

class Complicated(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fish(self, ctx):
        msg = await ctx.send("Bedobás...")
        await asyncio.sleep(random.randint(0, 2))
        await msg.edit("Horgászbot kitámasztása...")
        await asyncio.sleep(random.randint(0, 1))
        embed = discord.Embed(description="A csalit bedobtad a vízbe. Várj egy kis időt, amíg rákap egy hal. (5-20 másodperc)", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="🐟 A csali bent van!", icon_url=ctx.author.avatar_url)
        await msg.edit(embed=embed, content="Készenáll!")
        num = random.randint(-50, 150)
        if num > 90: num=90
        if num < 1: num=1
        lista = []
        for i in ftypes:
            if ftypes[i]["chance"] >= num: lista.append(ftypes[i]["name"])
        rand = random.choice(lista)
        stuff = []
        stuff.append(rand)
        stuff.append(ftypes[str(rand)]["value"])
        num2 = random.randint(-50, 150)
        if num2 > 80: num2=80
        if num2 < 1: num2=0.1
        lista2 = []
        for j in rarities:
            if rarities[j]["chance"] >= num2: lista2.append(rarities[j]["name"])
        rand2 = random.choice(lista2)
        stuff2 = []
        stuff2.append(rand2)
        stuff2.append(rarities[str(rand2)]["value"])
        hossz = random.randint(10, 500)
        await asyncio.sleep(random.randint(5, 20))
        embed2 = discord.Embed(description=f"Kifogtál egy **{stuff[0]}** halat!", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed2.add_field(name="Ritkaság", value=stuff2[0])
        embed2.add_field(name="Hossz", value=str(hossz)+"cm")
        embed2.add_field(name="Becsült eladási ár", value=(fish(stuff[1], hossz, stuff2[1])))
        await msg.edit(content=f"Kapás!", embed=embed2)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `inventory` WHERE user={ctx.author.id}")
        result = cursor.fetchall()
        itemid=result[2][0]+1
        cursor.execute(f"INSERT INTO `inventory` (user, item, id) VALUES ({ctx.author.id}, {stuff2[0]} {hossz} {(fish(stuff[1], hossz, stuff2[1]))}, {itemid}")
        db.commit()
        msg2=await ctx.send(ctx.author.mention)
        await msg2.delete()

    @commands.command()
    async def hunt(self, ctx):
        msg = await ctx.send("Állat keresése...")
        await asyncio.sleep(random.randint(0, 2))
        await msg.edit("Fegyver betöltése...")
        await asyncio.sleep(random.randint(0, 1))
        embed = discord.Embed(description="A fegyvert betöltötted. Várj, amíg meglátsz egy állatot. (5-20 másodperc)", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="🏹 Fegyver betöltve!", icon_url=ctx.author.avatar_url)
        await msg.edit(embed=embed, content="Készenáll!")
        num = random.randint(-50, 150)
        if num > 90: num=90
        if num < 1: num=1
        lista = []
        for i in atypes:
            if atypes[i]["chance"] >= num: lista.append(atypes[i]["name"])
        rand = random.choice(lista)
        stuff = []
        stuff.append(rand)
        stuff.append(atypes[str(rand)]["value"])
        num2 = random.randint(-50, 150)
        if num2 > 80: num2=80
        if num2 < 1: num2=0.1
        lista2 = []
        for j in rarities:
            if rarities[j]["chance"] >= num2: lista2.append(rarities[j]["name"])
        rand2 = random.choice(lista2)
        stuff2 = []
        stuff2.append(rand2)
        stuff2.append(rarities[str(rand2)]["value"])
        suly = random.randint(30, 150)
        await asyncio.sleep(random.randint(5, 20))
        embed2 = discord.Embed(description=f"Lelőttél egy **{stuff[0]}**-t!", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed2.add_field(name="Ritkaság", value=stuff2[0])
        embed2.add_field(name="Súly", value=str(suly)+"kg")
        embed2.add_field(name="Becsült eladási ár", value=(hunt(stuff[1], suly, stuff2[1])))
        await msg.edit(content=f"Lelőttél egy vadat!", embed=embed2)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `inventory` WHERE user={ctx.author.id}")
        result = cursor.fetchall()
        itemid=result[2][0]+1
        cursor.execute(f"INSERT INTO `inventory` (user, item, id) VALUES ({ctx.author.id}, {stuff2[0]} {suly} {(hunt(stuff[1], suly, stuff2[1]))}, {itemid}")
        db.commit()
        msg2=await ctx.send(ctx.author.mention)
        await msg2.delete()

    @commands.command()
    async def mine(self, ctx):
        msg = await ctx.send("Csákány elővétele...")
        await asyncio.sleep(random.randint(0, 2))
        await msg.edit("Élesítés...")
        await asyncio.sleep(random.randint(0, 1))
        embed = discord.Embed(description="Elkezdtél bányászni. Várj, míg meglátsz egy ércet. (5-20 másodperc)", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="⛏ Bányászás", icon_url=ctx.author.avatar_url)
        await msg.edit(embed=embed, content="Készenáll!")
        num = random.randint(-50, 150)
        if num > 90: num=90
        if num < 1: num=1
        lista = []
        for i in oretypes:
            if oretypes[i]["chance"] >= num: lista.append(oretypes[i]["name"])
        rand = random.choice(lista)
        stuff = []
        stuff.append(rand)
        stuff.append(oretypes[str(rand)]["value"])
        num2 = random.randint(-50, 150)
        if num2 > 80: num2=80
        if num2 < 1: num2=0.1
        lista2 = []
        for j in rarities:
            if rarities[j]["chance"] >= num2: lista2.append(rarities[j]["name"])
        rand2 = random.choice(lista2)
        stuff2 = []
        stuff2.append(rand2)
        stuff2.append(rarities[str(rand2)]["value"])
        suly = random.randint(1, 10)
        await asyncio.sleep(random.randint(5, 20))
        embed2 = discord.Embed(description=f"Kibányásztál egy **{stuff[0]}** ércet!", color=0xff9900, timestamp=datetime.datetime.utcnow())
        embed2.add_field(name="Ritkaság", value=stuff2[0])
        embed2.add_field(name="Súly", value=str(suly)+"kg")
        embed2.add_field(name="Becsült eladási ár", value=(mine(stuff[1], suly, stuff2[1])))
        await msg.edit(content="Siker!", embed=embed2)
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `inventory` WHERE user={ctx.author.id}")
        result = cursor.fetchall()
        itemid=result[2][0]+1
        cursor.execute(f"INSERT INTO `inventory` (user, item, id) VALUES ({ctx.author.id}, {stuff2[0]} {suly} {(mine(stuff[1], suly, stuff2[1]))}, {itemid}")
        db.commit()
        msg2=await ctx.send(ctx.author.mention)
        await msg2.delete()

    @commands.command()
    async def inventory(self, ctx):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `inventory` WHERE user={ctx.author.id}")
        result = cursor.fetchall()
        if len(result) == 0:
            await ctx.reply("A felhasználónak nincs semmi az eszköztárjában!", mention_author=False)
        else:
            embed = discord.Embed(color=0xff9900, timestamp=datetime.datetime.utcnow())
            xd = result[0][1].split(" ")
            for i in range(len(result)):
                embed.add_field(name=result[i][1], value=f"Ritkaság: **{xd[0]}**\nSúly/Hossz: **{xd[1]}**kg/cm\nBecsült eladási ár: **{xd[2]}**RC")
            embed.set_author(name="Eszköztár", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Inventory", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(Complicated(client))

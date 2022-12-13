import discord
from discord.ext import commands
import random
from main import db
import datetime
import asyncio

class Economy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["munka","dolgoz","dolgozás","dolgozas"])
    @commands.cooldown(1, 1800, type=commands.BucketType.user)
    async def work(self, ctx):
        randomszam = random.randint(50, 250)
        text = [f"Megkaptad a {randomszam}RC-d, amiért ügyesen dolgoztál!", f"Gratulálok, a fizetésed: {randomszam}RC!", f"Te voltál a hónap dolgozója ezért {randomszam}RC-t kaptál!", f'Munka helyett lazsáltál, de nyertél a RadonLottón és ezért {randomszam}RC-t kaptál!']
        randomtext = random.choice(text)
        workembed = discord.Embed(title="Munka", description=randomtext, color=0xFF9900, timestamp=datetime.datetime.utcnow())
        workembed.set_footer(text="Radon × Economy")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM economy_keszpenz WHERE user_id={}".format(ctx.author.id))
        result = cursor.fetchall()
        if (len(result) == 0):
            cursor.execute("INSERT INTO economy_keszpenz (user_id, egyenleg) values ({}, {})".format(ctx.author.id, randomszam))
            db.commit()
        else:
            ujosszeg = randomszam + result[0][1]
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(ujosszeg, ctx.author.id))
            db.commit()
        await ctx.reply(embed=workembed, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 2400, type=commands.BucketType.user)
    async def slut(self, ctx):
        randomszam = random.randint(150, 500)
        text = [f"Megcsaltad a barátod és ezért {randomszam}RC-t kaptál!", f"Lefeküdtél a miniszterelnökkel és tőle {randomszam}RC-t kaptál!", f"Összejöttél a főnököddel és ezért megemelte a fizetésed! Jutalmad {randomszam} RC!"]
        randomtext = random.choice(text)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM economy_keszpenz WHERE user_id={}".format(ctx.author.id))
        result = cursor.fetchall()
        if (len(result) == 0):
            cursor.execute("INSERT INTO economy_keszpenz (user_id, egyenleg) values ({}, {})".format(ctx.author.id, randomszam))
            db.commit()
        else:
            ujosszeg = randomszam + result[0][1]
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(ujosszeg, ctx.author.id))
            db.commit()
            workembed = discord.Embed(title="Ribanckodás", description=randomtext, color=0xFF9900, timestamp=datetime.datetime.utcnow())
            workembed.set_footer(text="Radon × Economy")
            await ctx.reply(embed=workembed, mention_author=False)

    @commands.command(aliases=["rablás", "betörés", "bűnözés"])
    @commands.cooldown(1, 3600, type=commands.BucketType.user)
    async def crime(self, ctx):
        randomszam = random.randint(350, 1000)
        text = [f"Elloptál egy értékes festményt, amit eladtál. Jutalmad: {randomszam}RC!", f"A barátaiddal kiraboltátok a bankot, ezért kaptál {randomszam}RC-t!", f'Megtámadtad a szomszédot és {randomszam} RC-t loptál!']
        randomtext = random.choice(text)
        cursor = db.cursor()
        cursor.execute("SELECT * FROM economy_keszpenz WHERE user_id={}".format(ctx.author.id))
        result = cursor.fetchall()
        if (len(result) == 0):
            cursor.execute("INSERT INTO economy_keszpenz (user_id, egyenleg) VALUES ({}, {})".format(ctx.author.id, randomszam))
            db.commit()
        else:
            ujosszeg = randomszam + result[0][1]
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(ujosszeg, ctx.author.id))
            db.commit()
        randomtext = random.choice(text)
        workembed = discord.Embed(title="Bűncselekmény", description=randomtext, color=0xFF9900, timestamp=datetime.datetime.utcnow())
        workembed.set_footer(text="Radon × Economy")
        await ctx.reply(embed=workembed, mention_author=False)

    @commands.command(aliases=["dep","betesz","bankbatesz"])
    async def deposit(self, ctx, money: int):
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT * FROM economy_keszpenz WHERE user_id={}".format(ctx.author.id))
        penztarca = cursor.fetchall()
        cursor.execute("SELECT * FROM economy_bank WHERE user_id={}".format(ctx.author.id))
        bank = cursor.fetchall()
        if (len(penztarca) == 0): 
            await ctx.reply("Nincs elég pénzed!") 
            return
        if money > penztarca[0][1]:
            await ctx.reply("Nincs elég pénzed!") 
            return
        if money < 0:
            await ctx.reply("Nem tehetsz be negatív összeget a bankba!") 
            return
        if len(bank) == 0:
            cursor.execute(f"INSERT INTO economy_bank (user_id, egyenleg) VALUES ({ctx.author.id}, {money})")
            asd = penztarca[0][1] - money
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(asd, ctx.author.id))
            db.commit()
            await ctx.reply(f"Sikeresen beraktál {money} összeget a bankba!")
        else:
            asd = penztarca[0][1] - money
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(asd, ctx.author.id))
            cursor.execute("UPDATE economy_bank SET egyenleg = {} WHERE user_id={}".format(bank[0][1] + money, ctx.author.id))
            db.commit()
            await ctx.reply(f"Sikeresen beraktál {money} összeget a bankba!")
    
    @commands.command(aliases=['with','kivesz','készpénzbetesz'])
    async def withdraw(self, ctx, money: int):
        cursor = db.cursor(buffered=True)
        cursor.execute(f"SELECT * FROM economy_keszpenz WHERE user_id={ctx.author.id}")
        penztarca = cursor.fetchall()
        cursor.execute(f"SELECT * FROM economy_bank WHERE user_id={ctx.author.id}")
        bank = cursor.fetchall()
        if (len(bank) == 0): 
            await ctx.reply("Nincs elég pénzed a bankban!")
            return
        if money > bank[0][1]:
            await ctx.reply("Nincs elég pénzed a bankban!") 
            return
        if money < 0:
            await ctx.reply("Nem tehetsz be negatív összeget a bankba!") 
            return
        if len(bank) == 0:
            await ctx.reply("Nincs elég pénzed a bankban!")
        else:
            asd = penztarca[0][1] + money
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(asd, ctx.author.id))
            cursor.execute("UPDATE economy_bank SET egyenleg = {} WHERE user_id={}".format(bank[0][1] - money, ctx.author.id))
            db.commit()
            await ctx.reply(f"Sikeresen kivettél {money}RC-t a bankodból")

    @commands.command(aliases=["balance", "bal", "egyenleg", "pénz", "rc", "rcbal"], usage=",balance")
    async def money(self, ctx, member: discord.User=None):
        if member == None:
            cursor = db.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM economy_keszpenz WHERE user_id={ctx.author.id}")
            penztarca = cursor.fetchall()
            cursor.execute(f"SELECT * FROM economy_bank WHERE user_id={ctx.author.id}")
            bank = cursor.fetchall()
            if (len(penztarca) == 0 and len(bank) == 0):
                    moneyEmbed = discord.Embed(title="Egyenleg", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                    moneyEmbed.add_field(name=":money_with_wings: Pénztárca", value=0, inline=False)
                    moneyEmbed.add_field(name=":bank: Bank", value=0,  inline=False)
                    moneyEmbed.set_footer(text="Radon × Economy")
                    moneyEmbed.set_thumbnail(url=ctx.author.avatar_url)
                    await ctx.reply(embed=moneyEmbed, mention_author=False)
            else:
                    
                    moneyEmbed = discord.Embed(title="Pénztárca", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                    try: moneyEmbed.add_field(name=":money_with_wings: Pénztárca", value=f"{penztarca[0][1]} RC", inline=False)
                    except: moneyEmbed.add_field(name=":money_with_wings: Pénztárca", value="0 RC", inline=False)
                    try: moneyEmbed.add_field(name=":bank: Bank", value=f"{bank[0][1]} RC", inline=False)
                    except: moneyEmbed.add_field(name=":bank: Bank", value="0 RC", inline=False)
                    moneyEmbed.set_footer(text="Radon × Economy")
                    moneyEmbed.set_thumbnail(url=ctx.author.avatar_url)
                    await ctx.reply(embed=moneyEmbed, mention_author=False)
        else:
            cursor = db.cursor(buffered=True)
            cursor.execute(f"SELECT * FROM economy_keszpenz WHERE user_id={member.id}")
            penztarca = cursor.fetchall()
            cursor.execute(f"SELECT * FROM economy_bank WHERE user_id={member.id}")
            bank = cursor.fetchall()
            if (len(penztarca) == 0 and len(bank) == 0):
                    moneyEmbed = discord.Embed(title="Egyenleg", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                    moneyEmbed.add_field(name=":money_with_wings: Pénztárca", value=0, inline=False)
                    moneyEmbed.add_field(name=":bank: Bank", value=0,  inline=False)
                    moneyEmbed.set_footer(text="Radon × Economy")
                    moneyEmbed.set_thumbnail(url=member.avatar_url)
                    await ctx.reply(embed=moneyEmbed, mention_author=False)
            else:
                    
                    moneyEmbed = discord.Embed(title="Pénztárca", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                    try: moneyEmbed.add_field(name=":money_with_wings: Pénztárca", value=f"{penztarca[0][1]} RC", inline=False)
                    except: moneyEmbed.add_field(name=":money_with_wings: Pénztárca", value="0 RC", inline=False)
                    try: moneyEmbed.add_field(name=":bank: Bank", value=f"{bank[0][1]} RC", inline=False)
                    except: moneyEmbed.add_field(name=":bank: Bank", value="0 RC", inline=False)
                    moneyEmbed.set_footer(text="Radon × Economy")
                    moneyEmbed.set_thumbnail(url=member .avatar_url)
                    await ctx.reply(embed=moneyEmbed, mention_author=False)

    @commands.command(aliases=["szerencse"], usage=',luck [tét]')
    @commands.cooldown(1, 60, type=commands.BucketType.user)
    async def luck(self, ctx, tét: int):
        if "-" in str(tét):
            await ctx.reply("Nem adhatsz meg mínusz számot!", mention_author=False)
            return
        if tét == 0:
            await ctx.reply("0 RC-vel nem játszhatsz!", mention_author=False)
            return
        cursor = db.cursor()
        asd = random.randint(1, 4)
        cursor.execute("SELECT * FROM economy_keszpenz WHERE user_id={}".format(ctx.author.id))
        result = cursor.fetchall()
        if len(result) == 0:
            moneyEmbed = discord.Embed(title="Hiba", description="Nincs elég pénzed!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
            moneyEmbed.set_footer(text="Radon × Economy")
            await ctx.reply(embed=moneyEmbed, mention_author=False)
        else:
            if result[0][1] >= tét:
                if asd in (1,2,3):
                    ok = result[0][1] - tét
                    cursor.execute(f"UPDATE economy_keszpenz SET egyenleg = {ok} WHERE user_id = {ctx.author.id}") 
                    db.commit()
                    moneyEmbed = discord.Embed(title="Szerencse", description=f"Vesztettél {tét}RC-t!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                    moneyEmbed.set_footer(text="Radon × Economy")
                    await ctx.reply(embed=moneyEmbed, mention_author=False)
                else:
                    ok = result[0][1] + tét
                    cursor.execute(f"UPDATE economy_keszpenz SET egyenleg = {ok} WHERE user_id = {ctx.author.id}")
                    db.commit()
                    moneyEmbed = discord.Embed(title="Szerencse", description=f"Nyertél {tét}RC-t!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                    moneyEmbed.set_footer(text="Radon × Economy")
                    await ctx.reply(embed=moneyEmbed, mention_author=False)
            else:
                moneyEmbed = discord.Embed(title="Hiba", description="Nincs elég pénzed!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
                moneyEmbed.set_footer(text="Radon × Economy")
                await ctx.reply(embed=moneyEmbed, mention_author=False)

    @commands.command(aliases=["add","addrc"])
    async def addmoney(self, ctx, money: int, user: discord.Member):
        if ctx.author.id in (648168353453572117, 654721418273226793, 609764483229024297, 406137394228625419):
            cursor = db.cursor()
            cursor.execute("SELECT * FROM economy_keszpenz WHERE user_id={}".format(user.id))
            result = cursor.fetchall() 
            if len(result) == 0:
                    cursor.execute("INSERT INTO economy_keszpenz (user_id, egyenleg) values ({}, {})".format(user.id, money))
                    db.commit()
                    await ctx.message.delete()
            else:
                    ujosszeg = money + result[0][1]
                    cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(ujosszeg, user.id))
                    db.commit()
                    await ctx.message.delete()
        else:
            return

    #napibér
    @commands.command(aliases=["napi"])
    @commands.cooldown(1, 86400, type=commands.BucketType.user)
    async def daily(self, ctx):
        randomszam = 750
        text = [f"Megkaptad a napi {randomszam}RC-d!"]
        randomtext = random.choice(text)
        workembed = discord.Embed(title="Napibér", description=randomtext, color=0xFF9900, timestamp=datetime.datetime.utcnow())
        workembed.set_footer(text="Radon × Economy")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM economy_keszpenz WHERE user_id={ctx.author.id}")
        result = cursor.fetchall()
        if (len(result) == 0):
            cursor.execute(f"INSERT INTO economy_keszpenz (user_id, egyenleg) values ({ctx.author.id}, {randomszam})")
            db.commit()
        else:
            ujosszeg = randomszam + result[0][1]
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(ujosszeg, ctx.author.id))
            db.commit()
        await ctx.reply(embed=workembed, mention_author=False)

    #órabér
    @commands.command(aliases=["órás","órai"])
    @commands.cooldown(1, 3600, type=commands.BucketType.user)
    async def hourly(self, ctx):
        randomszam = 500
        text = [f"Megkaptad az órabéred, ami {randomszam}RC!"]
        randomtext = random.choice(text)
        workembed = discord.Embed(title="Órabér", description=randomtext, color=0xFF9900, timestamp=datetime.datetime.utcnow())
        workembed.set_footer(text="Radon × Economy")
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM economy_keszpenz WHERE user_id={ctx.author.id}")
        result = cursor.fetchall()
        if (len(result) == 0):
            cursor.execute(f"INSERT INTO economy_keszpenz (user_id, egyenleg) values ({ctx.author.id}, {randomszam})")
            db.commit()
        else:
            ujosszeg = randomszam + result[0][1]
            cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(ujosszeg, ctx.author.id))
            db.commit()
        await ctx.reply(embed=workembed, mention_author=False)
    @commands.command(aliases=["guess", "guessnum", "gnum","numberguess","kitalalas"])
    async def szamkitalal(self, ctx):
        try:
            szam = random.randint(1, 100)
            cucc = ["A szám ennél kisebb.", "A szám ennél nagyobb.", "Eltaláltad!", "Ez a szám már volt."]
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            await ctx.reply(f"A számot kitaláltam. 15 másodperced lesz beírni az ötleteid.", mention_author=False)
            for i in range(1, 11):
                try:
                    msg = await self.client.wait_for('message', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Nem válaszoltál időben.')
                    return
                if int(msg.content) > szam and not i <= 0: await msg.reply(content=cucc[0] + f"\nHátralévő próbálkozások: {9-i}", mention_author=False)
                if int(msg.content) < szam and not i <= 0: await msg.reply(content=cucc[1] + f"\nHátralévő próbálkozások: {9-i}", mention_author=False)
                if int(msg.content) == szam and not i <= 0:
                    money = random.randint(100, 300)
                    await msg.reply(content=cucc[2] + " Nyertél **{}** RC-t.".format(money), mention_author=False)
                    cursor = db.cursor()
                    cursor.execute("SELECT * FROM economy_keszpenz WHERE user_id={}".format(ctx.author.id))
                    result = cursor.fetchall() 
                    if len(result) == 0:
                        cursor.execute("INSERT INTO economy_keszpenz (user_id, egyenleg) values ({}, {})".format(ctx.author.id, money))
                        db.commit()
                    else:
                        ujosszeg = money + result[0][1]
                        cursor.execute("UPDATE economy_keszpenz SET egyenleg = {} WHERE user_id={}".format(ujosszeg, ctx.author.id))
                        db.commit()
                    break
                i = i+1
                if i >= 10:
                    await ctx.send(f"Elfogytak a lehetőségek! A szám a **{szam}** volt.")
                    break
        except:
            pass

    @commands.command()
    async def additem(self, ctx):

        cursor = db.cursor()
        cursor.execute(f"SELECT item_id FROM shopid")
        item_id = cursor.fetchall()[0][0]+1
        cursor.execute(f"SELECT * FROM shop WHERE guild_id={ctx.guild.id}")
        result = cursor.fetchall()
        if len(result) >=10:
                await ctx.reply("Ezen a szerveren túl sok tárgy van beállítva!", mention_author=False)
                return
        messages = ["Kérlek add meg az áru nevét!", "Kérlek add meg a leírását. Ha nincs, írd hogy nincs.", "Kérlek add meg az árát a terméknek", "Kérlek add meg, hogy vásárláskor milyen rangot kapjon a vásárló, ha nincs írd hogy nincs! (`@rang` formátumban)"]
        for message in messages:
                await ctx.send(message)
                
                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try: msg = await self.client.wait_for("message", check=check, timeout=60)
                except asyncio.TimeoutError: break
                if message == "Kérlek add meg az áru nevét!":
                    nev = msg.content
                if message == "Kérlek add meg a leírását. Ha nincs, írd hogy nincs.":
                    if str(msg.content).lower() == "nincs":
                        leiras = "Nincs leírás"
                    else:
                        leiras = msg.content
                if message == "Kérlek add meg az árát a terméknek":
                    ar = msg.content
                if message == "Kérlek add meg, hogy vásárláskor milyen rangot kapjon a vásárló, ha nincs írd hogy nincs! (`@rang` formátumban)":
                    if str(msg.content).lower() == "nincs":
                        rang = "Nincs"
                    else:
                        rang = await commands.RoleConverter().convert(ctx, msg.content)
                        
        
        if rang == "Nincs": cursor.execute(f"""INSERT INTO shop (guild_id, nev, leiras, targy, ar, tipus, azonosito) VALUES ({ctx.guild.id}, "{str(nev)}", "{str(leiras)}", 0, {ar}, "nincs", {item_id})""")       
        else: cursor.execute(f"""INSERT INTO shop (guild_id, nev, leiras, targy, ar, tipus, azonosito) VALUES ({ctx.guild.id}, "{str(nev)}", "{str(leiras)}", {rang.id}, {ar}, "rang", {item_id})""")
        cursor.execute(f"UPDATE shopid SET item_id = {item_id}")
        db.commit()
        await ctx.reply("Tárgy beállítása sikeres!", mention_author=False)
        
    @commands.command()
    async def shop(self, ctx):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM shop WHERE guild_id={ctx.guild.id}")
        result = cursor.fetchall()
        if len(result) == 0:
            embed = discord.Embed(color=0xFF9900, timestamp=datetime.datetime.utcnow(), description="Ezen a szerveren egy tárgy sincs beállítva!")
            embed.set_author(name="Bolt", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Bolt", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)
            return
        else:
            embed = discord.Embed(color=0xFF9900, timestamp=datetime.datetime.utcnow())
            for x in range(len(result)):
                embed.add_field(name=f"{result[x][1]}", value=f"\nAzonosító: {result[x][6]}\n{result[x][2]}\nÁra: {result[x][4]} RC", inline=False)
                embed.set_author(name="Bolt", icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f"{ctx.author.name} × Bolt", icon_url=self.client.user.avatar_url)
            await ctx.send(embed=embed)
            
    @commands.command()
    async def buy(self, ctx, id):
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM economy_keszpenz WHERE user_id = {ctx.author.id}")
        penztarca = cursor.fetchall()
        cursor.execute(f"SELECT * FROM shop WHERE guild_id = {ctx.guild.id} AND azonosito = {id}")
        item = cursor.fetchall()
        if len(item) == 0: 
            await ctx.reply("Nem található ilyen azonosítóval rendelkező tárgy a boltban!")
            return
        
        item_price = item[0][4]
        item_type = item[0][6]
        if item_type == "nincs":
            item_role_id = "nincs"
        else:
            item_role_id = item[0][3]
        item_name = item[0][2]   
        item_id = item[0][7]
        if (len(penztarca) == 0 or item_price > penztarca[0][1]): 
            await ctx.reply("Nincs elég pénz nálad! Használd a `,withdraw` parancsot hogy felvehess a bankodból pénzt, vagy dolgozz.") 
            return
        if item_price < 0:
            await ctx.reply("Ennek a terméknek az ára negatív, ezért nem veheted meg!")
            return
        role = await commands.RoleConverter().convert(ctx, item_role_id)
        bot = await commands.MemberConverter().convert(ctx, 713014602891264051)
        if role.position > bot.top_role.position:
            await ctx.reply("Nem tudom rádadni a megvásárolt tárgy rangját. Kérlek szólj egy olyam rangúnak aki tudja kezelni a rangokat.")
            return
        await ctx.author.add_roles(role)
        cursor.execute(f"UPDATE economy_keszpenz SET egyenleg = {penztarca[0][1] - item_price} WHERE user_id={ctx.author.id}")
        db.commit()
        await ctx.reply("A tárgy megvásárlása sikeres volt!")
        
        

        
            

def setup(client):
    client.add_cog(Economy(client))

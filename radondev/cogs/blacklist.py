import discord
from discord.ext import commands
from main import db
import json

class Blacklist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def blreport(self, ctx, user=None, *,reason=None):
        try:
            user = await commands.UserConverter().convert(ctx, user)
        except:
            await ctx.send("<:radon_x:811191514482212874> A felhasználó nem található!")
            return
        msg = await ctx.send("Jelentésed elküldése folyamatban...")
        reportChannel = self.client.get_channel(818791448568266752)
        cursor = db.cursor()
        with open("number.json", "r") as f:
            number = json.load(f)
            case_id = number["number"] + 1
        cursor.execute("SELECT * FROM blacklist_queue")
        cursor.fetchall()
        cursor.execute("INSERT INTO blacklist_queue (case_id, user_id, reporter, reason) values ({}, {}, {}, '{}')".format(case_id, user.id, ctx.author.id, reason))
        db.commit()
        cursor.execute(f"SELECT * FROM blacklist_queue WHERE case_id={case_id}")
        result = cursor.fetchall()
        if (len(result) == 0):
            await ctx.send("<:radon_x:811191514482212874>Hiba történt a jelentésed elküldése közben! Kérlek próbáld meg újra!")
        else:
            user_id = result[0][1]
            case_id = result[0][0]
            dbreason = result[0][3]
            reporter = result[0][2]
            await reportChannel.send(f"Bejelentés érkezett!\nFelhasználó ID-je és neve: `{user_id}`, `{user.name}` \nBejelentő ID-je: {reporter}\nBejelentés ID: `{case_id}`\nIndok: `{dbreason}`")
            await msg.edit(content="Bejelentésed sikeresen elküldve! A jelentés állapotáról privát üzenetben értesítünk.")
            try: await ctx.author.send("Megkaptuk bejelentésed, állapotáról hamarosan értesítünk.")
            except: pass
        number["number"] = case_id
        with open("number.json", "w") as f:
            json.dump(number, f, indent=4)

    @commands.command()
    async def bldecline(self, ctx, id):
        if ctx.guild.id == 818791357836951603:
            msg = await ctx.send("Kérlek várj...")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM blacklist_queue WHERE case_id={id}")
            result = cursor.fetchall()
            if (len(result) == 0):
                await msg.edit(content="Ezzel az ID-val nem található bejelentés")
            else:
                cursor.execute(f"DELETE FROM blacklist_queue WHERE case_id={id}")
                db.commit()
                user = self.client.get_user(result[0][1])
                try: await user.send("Jelentésed állapota:\nA bejelentésed elutasításra került, a felhasználó nem került fel a feketelistára!")
                except: pass
                await msg.edit(content=f"Jelentés (ID: `{id}`) sikeresen elutasítva!")

    @commands.command()
    async def blaccept(self, ctx, id):
        if ctx.guild.id == 818791357836951603:
            msg = await ctx.send("Kérlek várj...")
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM blacklist_queue WHERE case_id={id}")
            result = cursor.fetchall()
            if (len(result) == 0):
                await msg.edit(content="Ezzel az ID-val nem található bejelentés")
            else:
                userid = result[0][1]
                uid = result[0][0]
                reason = result[0][3]
                
                cursor.execute(f"INSERT INTO blacklist (case_id, user_id, reason) values ({uid}, {userid}, '{reason}')")
                user = self.client.get_user(userid)
                db.commit()
                cursor.execute(f"DELETE FROM blacklist_queue WHERE case_id={id}")
                db.commit()
                try: await user.send("Jelentésed állapota:\nA bejelentésed elfogadásra került, a felhasználó felkerült a feketelistára!")
                except: pass
                await msg.edit(content=f"Jelentés (ID: `{id}`) sikeresen elfogadva!")

def setup(client):
    client.add_cog(Blacklist(client))
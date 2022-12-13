from discord.ext import commands
import discord
from main import db
import datetime

class Anti(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=",antiswear [be/ki]")
    async def antiswear(self, ctx, option):
        if ctx.author.guild_permissions.administrator:
            cursor = db.cursor()
            if str(option).lower() == "be":
                cursor.execute(f"SELECT *FROM antiswear WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if len(result) == 0:
                    cursor.execute(f"INSERT INTO antiswear (guild_id, valasz) VALUES ({ctx.guild.id}, 1)")
                    db.commit()
                    await ctx.reply("Sikeresen bekapcsoltad az anti káromkodás rendszert!", mention_author=False)
                else:
                    await ctx.reply("Már be van kapcsolva az anti káromkodás rendszer!", mention_author=False)
            elif str(option).lower() == "ki":
                cursor.execute(f"SELECT * FROM antiswear WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if not len(result) == 0:
                    cursor.execute(f"DELETE FROM antiswear WHERE guild_id={ctx.guild.id}")
                    db.commit()
                    await ctx.reply("Sikeresen kikapcsoltad az anti káromkodás rendszert!", mention_author=False)
                else:
                    await ctx.reply("Már ki van kapcsolva az anti káromkodás rendszer!", mention_author=False)
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",antilink [be/ki]")
    async def antilink(self, ctx, option):
        if ctx.author.guild_permissions.administrator:
            cursor = db.cursor()
            if str(option).lower() == "be":
                cursor.execute(f"SELECT * FROM antilink WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if len(result) == 0:
                    cursor.execute(f"INSERT INTO antilink (guild_id, valasz) VALUES ({ctx.guild.id}, 1)")
                    db.commit()
                    await ctx.reply("Sikeresen bekapcsoltad az anti link rendszert!", mention_author=False)
                else:
                    await ctx.reply("Már be van kapcsolva az anti link rendszer!", mention_author=False)
            elif str(option).lower() == "ki":
                cursor.execute(f"SELECT * FROM antilink WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if not len(result) == 0:
                    cursor.execute(f"DELETE FROM antilink WHERE guild_id={ctx.guild.id}")
                    db.commit()
                    await ctx.reply("Sikeresen kikapcsoltad az anti link rendszert!", mention_author=False)
                else:
                    await ctx.reply("Már ki van kapcsolva az anti link rendszer!", mention_author=False)
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",antispam [be/ki]")
    async def antispam(self, ctx, option):
        if ctx.author.guild_permissions.administrator:
            cursor = db.cursor()
            if str(option).lower() == "be":
                cursor.execute(f"SELECT * FROM antispam WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if len(result) == 0:
                    cursor.execute(f"INSERT INTO antispam (guild_id, valasz) VALUES ({ctx.guild.id}, 1)")
                    db.commit()
                    await ctx.send("Sikeresen bekapcsoltad az anti spam rendszert!")
                else:
                    await ctx.send("Már be van kapcsolva az anti spam rendszer!")
            elif str(option).lower() == "ki":
                cursor.execute(f"SELECT * FROM antispam WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if not len(result) == 0:
                    cursor.execute(f"DELETE FROM antispam WHERE guild_id={ctx.guild.id}")
                    db.commit()
                    await ctx.send("Sikeresen kikapcsoltad az anti antispam rendszert!")
                else:
                    await ctx.send("Már ki van kapcsolva az anti spam rendszer!")
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.command(usage=",bypass [@említés]")
    async def bypass(self, ctx, member):
        if ctx.author.guild_permissions.administrator:
            member = await commands.MemberConverter().convert(ctx, member)
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM bypassAutoMod WHERE guild_id={ctx.guild.id} AND user_id={member.id}")
            result = cursor.fetchall()
            if len(result) == 0:
                cursor.execute(f"INSERT INTO bypassAutoMod (guild_id, user_id) VALUES ({ctx.guild.id}, {member.id})")
                db.commit()
                await ctx.send(f"Sikeresen hozzáadtam {member.mention} felhasználót a listához. Mostantól ezen a szerveren az auto moderáció ignorálni fogja őt.")
            else:
                await ctx.send("Ez a felhasználó már a listán van!")
        else:
            db.commit()
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.command(usage=",removebypass [@említés]")
    async def removebypass(self, ctx, member):
        if ctx.author.guild_permissions.administrator:
            member = await commands.MemberConverter().convert(ctx, member)
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM bypassAutoMod WHERE guild_id={ctx.guild.id} AND user_id={member.id}")
            result = cursor.fetchall()
            if not len(result) == 0:
                cursor.execute(f"DELETE FROM bypassAutoMod WHERE guild_id={ctx.guild.id} AND user_id={member.id}")
                db.commit()
                await ctx.send(f"Sikeresen hozzáadtam {member.mention} felhasználót a listához. Mostantól ezen a szerveren az auto moderáció ignorálni fogja őt.")
            else:
                await ctx.send("Ez a felhasználó nincs a listán!")
        else:
            db.commit()
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.command(usage=',antiinvite [be/ki]')
    async def antiinvite(self, ctx, option):
        if ctx.author.guild_permissions.administrator:
            cursor = db.cursor()
            if str(option).lower() == "be":
                cursor.execute(f"SELECT * FROM antiinvite WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if len(result) == 0:
                    cursor.execute(f"INSERT INTO antiinvite (guild_id, valasz) VALUES ({ctx.guild.id}, 1)")
                    db.commit()
                    await ctx.send("Sikeresen bekapcsoltad az anti invite rendszert!")
                else:
                    await ctx.send("Már be van kapcsolva az anti invite rendszer!")
            elif str(option).lower() == "ki":
                cursor.execute(f"SELECT * FROM antiinvite WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if not len(result) == 0:
                    cursor.execute(f"DELETE FROM antiinvite WHERE guild_id={ctx.guild.id}")
                    db.commit()
                    await ctx.send("Sikeresen kikapcsoltad az anti invite rendszert!")
                else:
                    await ctx.send("Már ki van kapcsolva az anti invite rendszer!")
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

def setup(client):
    client.add_cog(Anti(client))
from discord.ext import commands
import discord
from discord.ext.commands.errors import MissingRequiredArgument
import mysql.connector as myc
import datetime
from main import db

class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=",setjoin <be/ki> <csatorna>")
    async def setjoin(self, ctx, option, channel: discord.TextChannel=None):
        if ctx.author.guild_permissions.administrator:
            if str(option).lower() == "be" and not channel == None:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM welcomeJoin WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if len(result) == 0:
                        cursor.execute(f"INSERT INTO welcomeJoin (guild_id, channel_id) VALUES ({ctx.guild.id}, {channel.id})")
                        db.commit()
                        await ctx.send("Sikeresen bekapcsoltad az üdvözlő rendszert!")
                else:
                        await ctx.send("Már be van kapcsolva az üdvözlő rendszer!")
            elif str(option).lower() == "ki" and channel == None:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM welcomeJoin WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if not len(result) == 0:
                        cursor.execute(f"DELETE FROM welcomeJoin WHERE guild_id={ctx.guild.id}")
                        db.commit()
                        await ctx.send("Sikeresen kikapcsoltad az üdvözlő rendszert!")
                else:
                        await ctx.send("Már ki van kapcsolva az üdvözlő rendszer!")
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.command(usage=",setleave <be/ki> <csatorna>")
    async def setleave(self, ctx, option, channel: discord.TextChannel=None):
        if ctx.author.guild_permissions.administrator:
            if str(option).lower() == "be" and not channel == None:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM welcomeLeave WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if len(result) == 0:
                        cursor.execute(f"INSERT INTO welcomeLeave (guild_id, channel_id) VALUES ({ctx.guild.id}, {channel.id})")
                        db.commit()
                        await ctx.send("Sikeresen bekapcsoltad a távozó rendszert!")
                else:
                        await ctx.send("Már be van kapcsolva a távozó rendszert!")
            elif str(option).lower() == "ki" and channel == None:
                cursor = db.cursor()
                cursor.execute(f"SELECT * FROM welcomeLeave WHERE guild_id={ctx.guild.id}")
                result = cursor.fetchall()
                if not len(result) == 0:
                        cursor.execute(f"DELETE FROM welcomeLeave WHERE guild_id={ctx.guild.id}")
                        db.commit()
                        await ctx.send("Sikeresen kikapcsoltad a távozó rendszert!")
                else:
                        await ctx.send("Már ki van kapcsolva a távozó rendszert!")
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

def setup(client):
    client.add_cog(Welcome(client))

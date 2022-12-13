import discord
from discord.ext import commands
import datetime
import random
import requests
import aiohttp
import asyncio
import urllib
import json

class Update(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command(aliases=["nick", "setnick"])
    async def setnickname(self, ctx, member: discord.Member, nick):
        await member.edit(nick=nick)
        await ctx.send(f'Siekresen megváltoztattam {member.mention} felhasználónak a nevét!')

    @commands.command(aliases=["dobokocka", "baszdfejbemagadat"])
    async def dice(self, ctx):
        await ctx.send(f"🎲 {random.randint(1, 6)}")

    @commands.command(usage=",mute <felhasználó> [indok: opcionális]")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Némított")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Némított")

            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
                await asyncio.sleep(2)
        embed = discord.Embed(title="Némítás", description=f"{member.mention} sikeresen le lett némítva ", colour=discord.Colour.light_gray())
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f"Le lettél némítva a **{guild.name}** szerveren!\n Indok: **{reason}**")

    @commands.command(usage=",unmute <felhasználó>")
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Némított")

        await member.remove_roles(mutedRole)
        await member.send(f"A némításod fel lett oldva a **{ctx.guild.name}** szerveren!")
        embed = discord.Embed(title="Némítás feloldása", description=f"Sikeresen feloldva {member.mention} a némítás alól",colour=discord.Colour.light_gray())
        await ctx.send(embed=embed)

    """@commands.command(aliases=["emoji", "em"], usage=",emote [emote]")
    async def emote(self, ctx, emoji):
        if emoji == "kekw":
            await ctx.send("<:radonkekw:816287486028283925>")
        elif emoji == "kegz":
            await ctx.send("<:kegz:818221733126864927>")
        elif emoji == "bruh":
            await ctx.send("<:bruh:818598903506796594>")
        elif emoji == "radon":
            await ctx.send("<:radon:808696830455709756>")
        elif emoji == "pog":
            await ctx.send("<:radonpog:818167191844945960>")
        elif emoji == "pepega":
            await ctx.send("<:pepega:822895067248853002>")
        elif emoji == "pepelaugh":
            await ctx.send("<:pepelaugh:822895206835683399>")
        elif emoji == "dom":
            await ctx.send("<:dom:822895290817708032>")
        elif emoji == "piknód" or emoji == "pn" or emoji == "picnode" or emoji == "piknod":
            await ctx.send("<:piknod:822895320870420480>")
        elif emoji == "hundreamlol" or emoji == "hundream":
            await ctx.send("<:hundreamlol:822895245079085097>")
        elif emoji == "pipa" or emoji == "ok":
            await ctx.send("<:radon_pipa:811191514369753149>")
        else:
            await ctx.send(f"A(z) `{emoji}` emoji nem található!")
        await ctx.message.delete()"""

    """@commands.command(usage=",warn [felhasználó] [üzenet]", aliases=["figyelmeztet"])
    async def warn(self, ctx, *, member, message):
        member = await commands.MemberConverter().convert(ctx, member)
        #warncount = db.fetch(f"FROM warns WHERE {member.id}_")
        if not ctx.message.author.bot:
            embed = discord.Embed(title="Figyelmeztetés", description=f"Figyelmeztetést kaptál a(z) {ctx.guild.name} szerverről, {ctx.author.name} felhasználótól. Indok: `{message}`", color=member.color, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text="Radon × Figyelmeztetés")
            await member.send(embed=embed)
        else:
            pass"""

    @commands.command(usage=[",mcszerver [szerver IP]"])
    async def mcszerver(self, ctx, szerver):
        r = requests.get(f"https://api.mcsrvstat.us/2/{szerver}")
        resp = r.json()
        embed = discord.Embed(title=f"{szerver} :link:", color=ctx.author.color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Játékosok", value=f"{resp['players']['online']}/{resp['players']['max']}")
        embed.add_field(name="MOTD", value=str(resp["motd"]["clean"]).replace("['", "").replace(",", "\n").replace("'", "").replace("'", "").replace("]", ""))
        embed.add_field(name="Verzió", value=resp["version"])
        await ctx.send(embed=embed)

#    @commands.command(aliases=["akasztofa"])
#    async def akasztófa

    @commands.command(usage=[",binary [szám]"], aliases=["bináris"])
    async def binary(self, ctx, content):
        szam = bin(content)
        embed=discord.Embed(title="Bináris kód", description="A szám bináris kódban: " + szam, color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
        await ctx.send(embed=embed)

    @commands.command(usage=[",kozososzto [első szám] [második szám]"], aliases=["kozos_oszto", "közösosztó", "közös_osztó", "lko"])
    async def kozososzto(self, ctx, szam1, szam2):
        for i in range(1,szam1):
            if szam1 % i == 0 and szam2 % i == 0:
                lko = i
        await ctx.send(f"A(z) {szam1} és a(z) {szam2} közös osztója: {lko}")

    @commands.command()
    async def bc(self, ctx):
        r = requests.get(f"https://api.mcsrvstat.us/2/play.birodalomcraft.hu")
        resp = r.json()
        embed = discord.Embed(title=f"BirodalomCraft szerver információjai <:birodalomcraft:775045871737634856>", color=ctx.author.color, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Játékosok", value=f"{resp['players']['online']}/{resp['players']['max']}")
        embed.add_field(name="MOTD", value=str(resp["motd"]["clean"]).replace("['", "").replace(",", "\n").replace("'", "").replace("'", "").replace("]", ""))
        embed.add_field(name="Verzió", value=resp["version"])
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/675056349196845096/825812713917644800/bc2_eredeti.png")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 300, type=commands.BucketType.user)
    async def hiba(self, ctx, *, uzenet):
        embed = discord.Embed(title=f"{ctx.author} hibát jelentett", color=ctx.author.color, timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.add_field(name="Hiba", value=uzenet)
        channel = self.client.get_channel(806906693191073862)
        await channel.send(embed=embed)

def setup(client):
    client.add_cog(Update(client))


from discord.ext import commands
import discord
import datetime
import asyncio
import random
from main import db
import json

def convert(time):
    pos = ["s","m","h","d"]
    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    return val * time_dict[unit]

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(usage=",warn [felhasználó] (indok)", aliases=["figyelmeztet", "figyelmeztetés", "figyelmeztetes"])
    async def warn(self, ctx, member: discord.Member, *, reason="Nincs indok megadva."):
        if ctx.author.guild_permissions.kick_members:
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            if member.id == ctx.author.id: await ctx.send("<:radon_x:856423841667743804> Magadat nem tudod figyelmeztetni!"); return
#            with open("/root/radon/radondev/cogs/modwarns.json") as r: data = json.load(r)
#            currentid = len(data)+1
#            with open("/root/radon/radondev/cogs/modwarns.json", "w") as f:
#                x = {
#                    ctx.guild.id: {
#                        currentid: {
#                            "warned": member.id,
#                            "warnedby": ctx.author.id,
#                            "warnid": currentid,
#                            "reason": str(reason)
#                        }
#                    }
#                }
#                json.dumps(x, indent=4)
            embed = discord.Embed(description=f"Figyelmeztetve lettél a **{ctx.guild.name}** szerveren.", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Figyelmeztetés indoka", value=f"`{reason}`", inline=False)
            embed.add_field(name="Figyelmeztetett téged", value=ctx.author)
#            embed.add_field(name="Figyelmeztetés ID", value=currentid)
            embed.set_author(name="Figyelmeztetés!", icon_url=ctx.guild.icon_url)
            embed.set_footer(text="Radon × Warn", icon_url=self.client.user.avatar_url)
            try:
                await member.send(embed=embed)
                embed2 = discord.Embed(description=f"{member.mention} figyelmeztetve lett {ctx.author.mention} által.", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed2.add_field(name="Indok", value=reason)
                embed2.set_author(name="Sikeres figyelmeztetés!", icon_url=ctx.author.avatar_url)
                embed2.set_footer(text=f"{ctx.author.name} × Figyelmeztetés", icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed2)
            except: await ctx.send(content=member.mention, embed=embed)
        else:
            perm = "Tagok kirúgása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",kick [felhasználó] (indok)", aliases=["kirúg", "kirug", "kirugás", "kirúgás", "kirúgas"])
    async def kick(self, ctx, member, *, reason="Nincs indok megadva."):
        if ctx.author.guild_permissions.kick_members:
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            bot = await ctx.guild.fetch_member(713014602891264051)
            if member.id == ctx.author.id: await ctx.reply("<:radon_x:856423841667743804> Magadat nem tudod kirúgni!", mention_author=False); return
            if member.top_role >= ctx.author.top_role: await ctx.reply("<:radon_x:856423841667743804> A felhasználónak van egy magasabb vagy ugyan olyan rangja, mint a te legfelső rangod!", mention_author=False); return
            if bot.top_role < member.top_role: await ctx.reply("<:radon_x:856423841667743804> A botnak kisebbek a rangjai, mint a felhasználónak!", mention_author=False); return
            if not bot.guild_permissions.kick_members: await ctx.reply("<:radon_x:856423841667743804> A botnak nincs joga kirúgáshoz!", mention_author=False); return
            else:
                try:
                    embed = discord.Embed(description=f"Ki lettél rúgva a **{ctx.guild.name}** szerverről!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                    embed.add_field(name="Általa", value=ctx.author, inline=False)
                    embed.add_field(name="Indok", value=f"`{reason}`", inline=False)
                    embed.set_author(name="Ki lettél rúgva!", icon_url=ctx.guild.icon_url)
                    embed.set_footer(text="Radon × Kirúgás", icon_url=self.client.user.avatar_url)
                    await member.send(embed=embed)
                except: pass
                await ctx.guild.kick(user=member, reason=reason)
                embed2 = discord.Embed(description=f"**{member.name}** ki lett rúgva **{ctx.author.name}** által!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                embed2.add_field(name="Indok", value=f"`{reason}`")
                embed2.set_author(name="Sikeres kirúgás!", icon_url=ctx.author.avatar_url)
                embed2.set_footer(text=f"{ctx.author.name} × Kirúgás", icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed2)
        else:
            perm = "Tagok kirúgása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",ban [felhasználó] (indok)", aliases=["kitilt", "kitiltás", "kitiltas"])
    async def ban(self, ctx, member, *, reason):
        if ctx.author.guild_permissions.ban_members:
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            bot = await ctx.guild.fetch_member(713014602891264051)
            if member.id == ctx.author.id: await ctx.reply("<:radon_x:856423841667743804> Magadat nem tudod kitiltani!", mention_author=False); return
            if member.top_role >= ctx.author.top_role: await ctx.reply("<:radon_x:856423841667743804> A felhasználónak van egy magasabb vagy ugyan olyan rangja, mint a te legfelső rangod!", mention_author=False); return
            if bot.top_role < member.top_role: await ctx.reply("<:radon_x:856423841667743804> A botnak kisebbek a rangjai, mint a felhasználónak!", mention_author=False); return
            if not bot.guild_permissions.ban_members: await ctx.reply("<:radon_x:856423841667743804> A botnak nincs joga kitiltáshoz!", mention_author=False); return
            else:
                try:
                    embed = discord.Embed(description=f"Ki lettél tiltva a **{ctx.guild.name}** szerverről!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                    embed.add_field(name="Általa", value=ctx.author, inline=False)
                    embed.add_field(name="Indok", value=f"`{reason}`", inline=False)
                    embed.set_author(name="Ki lettél tiltva!", icon_url=ctx.guild.icon_url)
                    embed.set_footer(text="Radon × Kitiltás", icon_url=self.client.user.avatar_url)
                    await member.send(embed=embed)
                except: pass
                await ctx.guild.ban(user=member, reason=reason, delete_message_days=0)
                embed2 = discord.Embed(description=f"**{member.name}** ki lett tiltva **{ctx.author.name}** által!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                embed2.add_field(name="Indok", value=f"`{reason}`")
                embed2.set_author(name="Sikeres kitiltás!", icon_url=ctx.author.avatar_url)
                embed2.set_footer(text=f"{ctx.author.name} × Kitiltás", icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed2)
        else:
            perm = "Tagok kitiltása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",tempban [felhasználó] [idő] (indok)")
    async def tempban(self, ctx, member, ido, *, reason):
        if ctx.author.guild_permissions.ban_members:
            try: ido=convert(ido)
            except: await ctx.reply("<:radon_x:856423841667743804> Helytelen időformátum!", mention_author=False); return
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            bot = await ctx.guild.fetch_member(713014602891264051)
            if member.id == ctx.author.id: await ctx.reply("<:radon_x:856423841667743804> Magadat nem tudod kitiltani!", mention_author=False); return
            if member.top_role >= ctx.author.top_role: await ctx.reply("<:radon_x:856423841667743804> A felhasználónak van egy magasabb vagy ugyan olyan rangja, mint a te legfelső rangod!", mention_author=False); return
            if bot.top_role < member.top_role: await ctx.reply("<:radon_x:856423841667743804> A botnak kisebbek a rangjai, mint a felhasználónak!", mention_author=False); return
            if not bot.guild_permissions.ban_members: await ctx.reply("<:radon_x:856423841667743804> A botnak nincs joga kitiltáshoz!", mention_author=False); return
            else:
                try:
                    embed = discord.Embed(description=f"Ki lettél tiltva a **{ctx.guild.name}** szerverről!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                    embed.add_field(name="Általa", value=ctx.author, inline=False)
                    embed.add_field(name="Indok", value=f"`{reason}`", inline=False)
                    embed.set_author(name="Ki lettél tiltva!", icon_url=ctx.guild.icon_url)
                    embed.set_footer(text="Radon × Kitiltás", icon_url=self.client.user.avatar_url)
                    await member.send(embed=embed)
                except: pass
                await ctx.guild.ban(user=member, reason=reason, delete_message_days=0)
                embed2 = discord.Embed(description=f"**{member.name}** ki lett tiltva **{ctx.author.name}** által!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                embed2.add_field(name="Indok", value=f"`{reason}`")
                embed2.set_author(name="Sikeres kitiltás!", icon_url=ctx.author.avatar_url)
                embed2.set_footer(text=f"{ctx.author.name} × Kitiltás", icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed2)
                await asyncio.sleep(ido)
                await ctx.guild.unban(member)
        else:
            perm = "Tagok kitiltása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",softban [felhasználó] (indok)")
    async def softban(self, ctx, member, *, reason):
        if ctx.author.guild_permissions.ban_members:
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            bot = await ctx.guild.fetch_member(713014602891264051)
            if member.id == ctx.author.id: await ctx.reply("<:radon_x:856423841667743804> Magadat nem tudod kitiltani!", mention_author=False); return
            if member.top_role >= ctx.author.top_role: await ctx.reply("<:radon_x:856423841667743804> A felhasználónak van egy magasabb vagy ugyan olyan rangja, mint a te legfelső rangod!", mention_author=False); return
            if bot.top_role < member.top_role: await ctx.reply("<:radon_x:856423841667743804> A botnak kisebbek a rangjai, mint a felhasználónak!", mention_author=False); return
            if not bot.guild_permissions.ban_members: await ctx.reply("<:radon_x:856423841667743804> A botnak nincs joga kitiltáshoz!", mention_author=False); return
            else:
                try:
                    embed = discord.Embed(description=f"Ki lettél tiltva a **{ctx.guild.name}** szerverről!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                    embed.add_field(name="Általa", value=ctx.author, inline=False)
                    embed.add_field(name="Indok", value=f"`{reason}`", inline=False)
                    embed.set_author(name="Ki lettél tiltva!", icon_url=ctx.guild.icon_url)
                    embed.set_footer(text="Radon × Kitiltás", icon_url=self.client.user.avatar_url)
                    await member.send(embed=embed)
                except: pass
                await ctx.guild.ban(user=member, reason=reason, delete_message_days=7)
                embed2 = discord.Embed(description=f"**{member.name}** ki lett tiltva **{ctx.author.name}** által!", timestamp=datetime.datetime.utcnow(), color=0xff9900)
                embed2.add_field(name="Indok", value=f"`{reason}`")
                embed2.set_author(name="Sikeres kitiltás!", icon_url=ctx.author.avatar_url)
                embed2.set_footer(text=f"{ctx.author.name} × Kitiltás", icon_url=self.client.user.avatar_url)
                await ctx.send(embed=embed2)
        else:
            perm = "Tagok kitiltása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",mute [felhasználó] (indok)", aliases=["némítás", "nemitas", "nemítás", "nemitás", "némitas", "némítas", "némitás"])
    async def mute(self, ctx, member, *, reason="Nincs indok megadva"):
        if ctx.author.guild_permissions.kick_members:
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            bot = await ctx.guild.fetch_member(713014602891264051)
            if member.id == ctx.author.id: await ctx.reply("<:radon_x:856423841667743804> Magadat nem tudod lenémítani!", mention_author=False); return
            if member.top_role >= ctx.author.top_role: await ctx.reply("<:radon_x:856423841667743804> A felhasználónak van egy magasabb vagy ugyan olyan rangja, mint a te legfelső rangod!", mention_author=False); return
            if bot.top_role < member.top_role: await ctx.reply("<:radon_x:856423841667743804> A botnak kisebbek a rangjai, mint a felhasználónak!", mention_author=False); return
            if not bot.guild_permissions.manage_roles: await ctx.reply("<:radon_x:856423841667743804> A botnak nincs joga rangok adásához!", mention_author=False); return
            else:
                embed = discord.Embed(description=f"{member.mention} le lett némítva {ctx.author.mention} által!", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name="Némítás", icon_url=ctx.author.avatar_url)
                embed.add_field(name="Indok", value=f"`{reason}`")
                embed.set_footer(text=f"{ctx.author.name} × Némítás", icon_url=self.client.user.avatar_url)
                if not discord.utils.get(ctx.guild.roles, name="Némított"):
                    msg = await ctx.reply("Kérlek várj, amíg létrehozom a rangot és bekonfigurálom a rendszert...", mention_author=False)
                    mutedrole = await ctx.guild.create_role(name="Némított", colour=0xff9900, reason=f"Némítás - {ctx.author.name} - Egyszeri alkalom")
                    overwrites = {
                        mutedrole: discord.PermissionOverwrite(send_messages=False)
                    }
                    for i in ctx.guild.channels: await i.edit(overwrites=overwrites)
                    await msg.delete()
                await member.add_roles(discord.utils.get(ctx.guild.roles, name="Némított"))
                await ctx.reply(embed=embed, mention_author=False)
        else:
            perm = "Tagok kirúgása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",tempmute [felhasználó] [idő] (indok)")
    async def tempmute(self, ctx, member, ido, *, reason="Nincs indok megadva"):
        if ctx.author.guild_permissions.kick_members:
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            bot = await ctx.guild.fetch_member(713014602891264051)
            if member.id == ctx.author.id: await ctx.reply("<:radon_x:856423841667743804> Magadat nem tudod lenémítani!", mention_author=False); return
            if member.top_role >= ctx.author.top_role: await ctx.reply("<:radon_x:856423841667743804> A felhasználónak van egy magasabb vagy ugyan olyan rangja, mint a te legfelső rangod!", mention_author=False); return
            if bot.top_role < member.top_role: await ctx.reply("<:radon_x:856423841667743804> A botnak kisebbek a rangjai, mint a felhasználónak!", mention_author=False); return
            if not bot.guild_permissions.manage_roles: await ctx.reply("<:radon_x:856423841667743804> A botnak nincs joga rangok adásához!", mention_author=False); return
            else:
                embed = discord.Embed(description=f"{member.mention} le lett némítva {ctx.author.mention} által!", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name="Némítás", icon_url=ctx.author.avatar_url)
                embed.add_field(name="Indok", value=f"`{reason}`")
                embed.add_field(name="Időtartam", value=ido)
                embed.set_footer(text=f"{ctx.author.name} × Némítás", icon_url=self.client.user.avatar_url)
                if not discord.utils.get(ctx.guild.roles, name="Némított"):
                    msg = await ctx.reply("Kérlek várj, amíg létrehozom a rangot és bekonfigurálom a rendszert...", mention_author=False)
                    mutedrole = await ctx.guild.create_role(name="Némított", colour=0xff9900, reason=f"Némítás - {ctx.author.name} - Egyszeri alkalom")
                    overwrites = {
                        mutedrole: discord.PermissionOverwrite(send_messages=False)
                    }
                    for i in ctx.guild.channels: await i.edit(overwrites=overwrites)
                    await msg.delete()
                try: ido=convert(ido)
                except: await ctx.reply("<:radon_x:856423841667743804> Helytelen időformátum!", mention_author=False); return
                await member.add_roles(discord.utils.get(ctx.guild.roles, name="Némított"))
                await ctx.reply(embed=embed, mention_author=False)
                await asyncio.sleep(ido)
                await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Némított"))
        else:
            perm = "Tagok kirúgása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",unmute [felhasználó]")
    async def unmute(self, ctx, member):
        if ctx.author.guild_permissions.kick_members:
            try: member = await commands.MemberConverter().convert(ctx, member)
            except: 
                embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
                embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed1, mention_author=False)
                return
            bot = await ctx.guild.fetch_member(713014602891264051)
            if member.top_role >= ctx.author.top_role: await ctx.reply("<:radon_x:856423841667743804> A felhasználónak van egy magasabb vagy ugyan olyan rangja, mint a te legfelső rangod!", mention_author=False); return
            if bot.top_role < member.top_role: await ctx.reply("<:radon_x:856423841667743804> A botnak kisebbek a rangjai, mint a felhasználónak!", mention_author=False); return
            if not bot.guild_permissions.manage_roles: await ctx.reply("<:radon_x:856423841667743804> A botnak nincs joga rangok adásához!", mention_author=False); return
            else:
                embed = discord.Embed(description=f"{member.mention} némítása fel lett oldva {ctx.author.mention} által!", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name="Némítás feloldása", icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f"{ctx.author.name} × Némítás", icon_url=self.client.user.avatar_url)
                if discord.utils.get(ctx.guild.roles, name="Némított"):
                    try:
                        await member.remove_roles(discord.utils.get(ctx.guild.roles, name="Némított"))
                    except:
                        await ctx.reply("A felhasználón nincsen rajta némított nevű rang!")
                        return
                else:
                    await ctx.reply("A szerveren időközben törölték a rangot! Mondjuk nem tudom, hogy ezt hogyan sikerült. gg lol")
                    return
                await ctx.reply(embed=embed, mention_author=False)
        else:
            perm = "Tagok kirúgása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",unban [felhasználónév és tag, pl. Radon#6074", aliases=["ub", "felold", "kitiltasfelold", "kitiltásfelold", "feloldás"])
    async def unban(self, ctx, user):
        if ctx.author.guild_permissions.ban_members == False: 
            perm = "Tagok kitiltása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        else:
            if user.isdigit() == False: 
                lista = user.split('#')
                if len(lista) != 2: 
                    embed = discord.Embed(description="Nem található ilyen felhasználó a kitiltottak listáján! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)
                    return
                else: 
                    member_name = lista[0]
                    member_discriminator = lista[1]
                    banned_users = await ctx.guild.bans()
                    asd = False
                    for ban in banned_users:
                        if (ban.user.name, ban.user.discriminator) == (member_name, member_discriminator):
                            await ctx.guild.unban(ban.user)
                            embed = discord.Embed(timestamp = datetime.datetime.utcnow(), color = 0xff9900, description = f"`{ban.user.name}#{ban.user.discriminator}` kitiltása `{ctx.author.name}#{ctx.author.discriminator}` által feloldásra került!")
                            embed.set_author(name="Kitiltás feloldása", icon_url=ctx.author.avatar_url)
                            embed.set_footer(text=f"{ctx.author} × Kitiltás feloldása", icon_url=self.client.user.avatar_url)
                            await ctx.reply(embed=embed, mention_author=False)
                            asd = True
                            await user.send(f"A kitiltásod feloldották a **{ctx.author.guild_name}** szerveren!")
                    if asd == False:                         
                        embed = discord.Embed(description="Nem található ilyen felhasználó a kitiltottak listáján! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                        embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                        await ctx.reply(embed=embed, mention_author=False)
                        return
            else:
                banned_users = await ctx.guild.bans()
                lista = [b.user.id for b in banned_users]
                if int(user) not in lista: 
                    embed = discord.Embed(description="Nem található ilyen felhasználó a kitiltottak listáján! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)
                    return
                else:
                    user = await self.client.fetch_user(user)
                    await ctx.guild.unban(user)
                    embed = discord.Embed(timestamp = datetime.datetime.utcnow(), color = 0xff9900, description = f"`{user.name}#{user.discriminator}` kitiltása `{ctx.author.name}#{ctx.author.discriminator}` által feloldásra került!")
                    embed.set_author(name="Kitiltás feloldása", icon_url=ctx.author.avatar_url)
                    embed.set_footer(text=f"{ctx.author} × Kitiltás feloldása", icon_url=self.client.user.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def unbanall(self, ctx):
        if ctx.author.guild_permissions.ban_members:
            msg = await ctx.reply(content="<a:loadwhite:856423043273195530> Kérlek, várj...", mention_author=False)
            for member in await ctx.guild.bans():
                await ctx.guild.unban(member.user)
                await asyncio.sleep(2)
            await msg.edit("<:radon_check:856423841612824607> Sikeresen feloldottam az összes felhasználót!")
        else:
            perm = "Tagok kitiltása"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",nickall (becenevek, ha nincs megadva, kiaadja a lehetőségeket)", aliases=["setnickall"])
    async def nickall(self, ctx, *, nick=None):
        if nick==None:
            await ctx.reply(f"> Felhasználó nevének megjelenítése: `[membername]`\n> Pl. 'Tag | [membername]' így lesz megjelenítve a Radon számára: `Tag | Radon`, a tiéd pedig így fog kinézni: `Tag | {ctx.author.name}`", mention_author=False)
        if ctx.author.guild_permissions.manage_nicknames:
            msg = await ctx.reply(content="Kérlek várj...", mention_author=False)
            for member in ctx.guild.members:
                xd=nick.replace("[membername]", member.name)
                await member.edit(nick=xd)
                await asyncio.sleep(1)
            await msg.edit(f"Sikeresen átneveztem az összes felhasználót! (`{xd}`)")
        else:
            perm = "Becenevek kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",nick [felhasználó] (becenév, ha nincs megadva, kiaadja a lehetőségeket)", aliases=["nickname", "setnick", "setnickname"])
    async def nick(self, ctx, member, *, nick=None):
        if nick==None: await ctx.reply(f"> Felhasználó nevének megjelenítése: `[membername]`\n> Pl. 'Tag | [membername]' így lesz megjelenítve a Radon számára: `Tag | Radon`, a tiéd pedig így fog kinézni: `Tag | {ctx.author.name}`", mention_author=False)
        try: member = await commands.MemberConverter().convert(ctx, member)
        except:
            embed1 = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
            embed1.set_author(name="Hiba!", icon_url=self.client.user.avatar_url)
            embed1.set_footer(text=f"{ctx.author.name} × Hiba", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed1, mention_author=False)
            return
        if ctx.author.guild_permissions.manage_nicknames:
            xd=nick.replace("[membername]", member.name)
            if nick=="clear" or nick=="töröl": await member.edit(nick=None); await ctx.reply("A tag becenevét töröltem!", mention_author=False)
            await member.edit(nick=xd)
            await ctx.reply(f"A tagot sikeresen átneveztem! Új becenév: `{xd}`", mention_author=False)
        else:
            perm = "Becenevek kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
            return

    @commands.command(usage=",addrole [@említés] [@rang]")
    async def addrole(self, ctx, user, *, role):   
        if ctx.author.guild_permissions.manage_roles == False: 
            perm = "Rangok kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        else:
            try: user = await commands.MemberConverter().convert(ctx, user)
            except: 
                embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            try: role = await commands.RoleConverter().convert(ctx, role)
            except:
                embed = discord.Embed(description="Nem található ilyen rang a szerveren! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed = embed, mention_author=False)
                return
            if ctx.author.id == user.id: 
                embed = discord.Embed(description="Nem adhatsz magadnak rangot! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            elif ctx.author.guild.owner == False:
                if ctx.author.top_role < role: 
                    embed = discord.Embed(description="Ez a rang magasabb mint a te rangod, ezért nem adhatod oda másnak! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)
                    return
            else:
                pass
            bot = await commands.MemberConverter().convert(ctx, str(713014602891264051))
            if bot.guild_permissions.manage_roles == False: 
                embed = discord.Embed(description="Nincs jogosultságom a felhasználó kezelésére! <:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            await user.add_roles(role)
            embed = discord.Embed(description=f":white_check_mark: {role.mention} sikeresen odaadva {user.mention} számára!", timestamp = datetime.datetime.utcnow(), color=0xff9900)
            embed.set_author(name="Rang adás", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author} × Rang adás", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",removerole [@említés] [@rang]")
    async def removerole(self, ctx, user, *, role):   
        if ctx.author.guild_permissions.manage_roles == False: 
            perm = "Rangok kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        else:
            try: user = await commands.MemberConverter().convert(ctx, user)
            except: 
                embed = discord.Embed(description="Nem található ilyen felhasználó a szerveren!<:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            try: role = await commands.RoleConverter().convert(ctx, role)
            except:
                embed = discord.Embed(description="Nem található ilyen rang a szerveren!<:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed = embed, mention_author=False)
                return
            if ctx.author.id == user.id: 
                embed = discord.Embed(description="Nem vehetsz le magadról rangot!<:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            elif ctx.author.guild.owner == False:
                if ctx.author.top_role < role: 
                    embed = discord.Embed(description="Ez a rang magasabb mint a te rangod, ezért nem veheted le másról!<:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                    embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                    await ctx.reply(embed=embed, mention_author=False)
                    return
            else:
                pass
            bot = await commands.MemberConverter().convert(ctx, str(713014602891264051))
            if bot.guild_permissions.manage_roles == False: 
                embed = discord.Embed(description="Nincs jogosultságom a felhasználó kezelésére!<:radon_x:811191514482212874>", color=0xff9900, timestamp=datetime.datetime.utcnow())
                embed.set_author(name=f"Hiba × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)
                await ctx.reply(embed=embed, mention_author=False)
                return
            await user.remove_roles(role)
            embed = discord.Embed(description=f":white_check_mark:{role.mention} sikeresen elvéve {user.mention}-tól/-től!", timestamp = datetime.datetime.utcnow(), color=0xff9900)
            embed.set_author(name="Rang elvétel", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author} × Rang elvétel", icon_url=self.client.user.avatar_url)
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",roleall [@rang]")
    async def roleall(self, ctx, role):
        if ctx.author.guild_permissions.manage_roles:
            role = await commands.RoleConverter().convert(ctx, role)
            await ctx.reply("Kérlek várj...")
            for member in ctx.guild.members:
                try: await member.add_roles(role)
                except: continue
                await asyncio.sleep(1)
            await ctx.send(f"Sikeresen megkapta az összes felhasználó a {role.name} rangot!")
        else:
            perm = "Rangok kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",removeroleall [@rang]", aliases=["removeall"])
    async def removeroleall(self, ctx, role):
        if ctx.author.guild_permissions.manage_roles:
            role = await commands.RoleConverter().convert(ctx, role)
            await ctx.reply("Kérlek várj...")
            for member in ctx.guild.members:
                try: await member.remove_roles(role)
                except: continue
                await asyncio.sleep(1)
            await ctx.send(f"Sikeresen elvettem az összes felhasználótól a {role.name} rangot!")
        else:
            perm = "Rangok kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)

    @commands.command(usage=",slowmode [idő másodpercben]", aliases=["slow", "slowmode", "sm"])
    async def lassítás(self, ctx, time:int):
        if not ctx.author.guild_permissions.manage_channels:
            perm = "Csatornák kezelése"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        else:
            if time == 0:
                await ctx.reply("Lassítás: **kikapcsolva**")
                await ctx.channel.edit(slowmode_delay = 0)
            elif time > 21600:
                await ctx.reply('Nem tudsz 6 óránál nagyobb lassítást beállítani!')
                return
            else:
                await ctx.channel.edit(slowmode_delay = time)
                await ctx.reply(f'Lassítás: **{time}mp**')

def setup(client):
    client.add_cog(Moderation(client))      

import discord
from discord.ext import commands
import json

class Whitelist(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def whitelist(self, ctx, option, user=None):
        if ctx.author.guild_permissions.administrator:
            if option.lower() == "be":
                with open("whitelist.json", "r") as f:
                    wh = json.load(f)
                try:
                    wh[str(ctx.guild.id)]
                    await ctx.send("Már be van kapcsolva a whitelist funkció!")
                    return
                except:
                    wh[str(ctx.guild.id)] = {} 
                    wh[str(ctx.guild.id)][str(ctx.author.id)] = {}
                    with open("whitelist.json", "w") as f:
                        json.dump(wh, f, indent=4)
                    await ctx.send("A whitelist rendszer beállításra került!")
            elif option.lower() == "add" and not user == None:
                try: user = await commands.UserConverter().convert(ctx, user)
                except: await ctx.send("Felhasználó nem található!")
                with open("whitelist.json") as f:
                    wh = json.load(f)
                try: 
                    wh[str(ctx.guild.id)]
                    wh[str(ctx.guild.id)][str(user.id)] = {}
                    with open("whitelist.json", "w") as f:
                        json.dump(wh, f, indent=4)
                    await ctx.send(f" {user.mention} hozzáadva a listához")
                except: await ctx.send("Ki van kapcsolva a whitelist rendszer!")
            elif option.lower() == "remove" and not user == None:
                try: user = await commands.UserConverter().convert(ctx, user)
                except: await ctx.send("Felhasználó nem található!")
                with open("whitelist.json") as f:
                    wh = json.load(f)
                try: 
                    del wh[str(ctx.guild.id)][str(user.id)]
                    with open("whitelist.json", "w") as f:
                        json.dump(wh, f, indent=4)
                    await ctx.send(f" {user.mention} levéve a listáról")
                except: await ctx.send("Ki van kapcsolva a whitelist rendszer, vagy a felhasználó nincs a rendszerben!")
            elif option.lower() == "ki":
                with open("whitelist.json") as f:
                    wh = json.load(f)
                try: 
                    wh.pop(str(ctx.guild.id))
                    with open("whitelist.json", "w") as f:
                        json.dump(wh, f, indent=4)
                    await ctx.send(f"Whitelist rendszer kikapcsolva!")
                except: 
                    await ctx.send("Már ki van kapcsolva a whitelist rendszer!")
                    raise
        else:
            perm = "Adminisztrátor"
            embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('whitelist.json', "r") as f:
            wh = json.load(f)
        try:
            wh[str(member.guild.id)]
            try:
                wh[str(member.guild.id)][str(member.id)]
                return
            except:
                await member.kick(reason="Whitelist")
                try: await member.send("Nem szerepelsz a szerver fehérlistáján, ezért nem léphetsz be erre a szerverre!")        
                except: return
        except:
            return

def setup(client):
    client.add_cog(Whitelist(client))

import discord
from discord.ext import commands
from datetime import timedelta
import asyncio
import random
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

def save_db(time, msgid):
    with open("gw.json", "r") as f:
        db = json.load(f)
        db[str(msgid)] = {}
        db[str(msgid)]["time"] = time
    with open("gw.json", "w") as f:
        json.dump(db, f, indent=4)

    
class Giveaway(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def giveaway(self, ctx):
        try:
            await ctx.send("Minden kérdésre fél perced lesz válaszolni. A válaszokat a chatbe, prefix __nélkül__ írdd!")
            kerdesek = ["Melyik csatornában legyen a nyereményjáték?", "Mennyi idő legyen a nyereményjáték? (s|m|h|d)", "Mi legyen a nyeremény?"]
            valaszok = []
            def check(m): return m.author == ctx.author and m.channel == ctx.channel
            for i in kerdesek:
                await ctx.send(i)
                try:
                    msg = await self.client.wait_for('message', timeout=30.0, check=check)
                except asyncio.TimeoutError:
                    await ctx.send('Nem válaszoltál időben, a nyereményjáték készítő bezárul.')
                    return
                else: 
                    if '@' in msg.content:
                        await ctx.send("felejtős")
                        return
                    valaszok.append(msg.content)
            try:
                channel_id = int(valaszok[0][2:-1])
            except:
                await ctx.send(f"Hibás csatornaformátum! Használj {ctx.channel.mention}-t!")
                return
            channel = self.client.get_channel(channel_id)
            time = convert(valaszok[1])
            if time == -1:
                await ctx.send(f"Hibás időformátum! s|m|h|d")
                return
            elif time == -2:
                await ctx.send(f"Hibás időformátum! s|m|h|d ")
                return
            nyeremeny = valaszok[2]
            await ctx.send(f"A nyereményjáték a {channel.mention}-ban/ben készen áll!")
            embed = discord.Embed(title = "Nyereményjáték!", description = f"{nyeremeny}", color = 0xFF9900)
            embed.add_field(name = "Indította:", value = ctx.author.mention)
            embed.add_field(name = "Ideje:", value = valaszok[1])
            botmsg = await channel.send(embed = embed)
            await botmsg.add_reaction("🎉")
            await asyncio.sleep(time)
            new_msg = await channel.fetch_message(botmsg.id)
            try:
                felhasznalok = await new_msg.reactions[0].users().flatten()
                felhasznalok.pop(felhasznalok.index(self.client.user))
                winner = random.choice(felhasznalok)
            except:
                await channel.send("Senki nem jelentkezett, így senki sem nyert!")
                return
            await channel.send(f"Gratulálok! {winner.mention} nyerte meg a következőt: **{nyeremeny}**!")
        except:
            raise



    @commands.command(usage=",reroll <csatorna> <nyereményjáték üzenet id>")
    async def reroll(self, ctx, channel : discord.TextChannel, messageid : int):
        try:
            new_msg = await channel.fetch_message(messageid)
        except:
            await ctx.send("Nem található ilyen üzenet ID")
        try:
            felhasznalok = await new_msg.reactions[0].users().flatten()
            felhasznalok.pop(felhasznalok.index(self.client.user))
            winner = random.choice(felhasznalok)
        except:
            await channel.send("Senki nem jelentkezett, így senki sem nyert!")
            return
        await channel.send(f"Az új nyertes: {winner.mention}")

    @commands.command(usage=",mansorsol <csatorna> <nyereményjáték üzenet id>")
    async def mansorsol(self, ctx, channel : discord.TextChannel, messageid : int):
        try:
            new_msg = await channel.fetch_message(messageid)
        except:
            await ctx.send("Nem található ilyen üzenet ID")
        try:
            felhasznalok = await new_msg.reactions[0].users().flatten()
            felhasznalok.pop(felhasznalok.index(self.client.user))
            winner = random.choice(felhasznalok)
        except:
            await channel.send("Senki nem jelentkezett, így senki sem nyert!")
            return
        await channel.send(f"Gratulálok! {winner.mention} nyerte meg a nyereményjátékot!")

def setup(client):
    client.add_cog(Giveaway(client))

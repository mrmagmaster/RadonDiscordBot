import asyncio
import discord
from discord.errors import ConnectionClosed, GatewayNotFound
from discord.ext import commands
from discord_components import DiscordComponents
import os
import datetime
import random
import mysql.connector as myc
import schedule
from discord.ext import tasks
from discord_slash import SlashCommand
import sys

a = []

"""logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))
logger.addHandler(handler)
import subprocess
import select
logger.info(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))"""

def task():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM rc")
    cursor.fetchall()
    db.commit()

def get_prefix(client, ctx):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM `prefix` WHERE server_id={int(ctx.guild.id)}")
    result = cursor.fetchall()
    if len(result) == 0:
        default_prefix = ","
        cursor = db.cursor()
        cursor.execute("INSERT INTO prefix (server_id, prefix) VALUES (%s, %s)", (int(ctx.guild.id), default_prefix))
        db.commit()
        return default_prefix
    else:
        return result[0][1]


db = myc.connect(host="localhost", user="root",
    password="OPiutkmcfjue487ik5",
    db="db")

intents = discord.Intents()
intents.messages = True
intents.guilds = True
intents.reactions = True

client = commands.AutoShardedBot(command_prefix=".", case_insensitive=True, intents = discord.Intents().all())
slash = SlashCommand(client, override_type = True, sync_commands=True)
client.remove_command("help")
        
blacklist = [ ]
x = 1
disabled_prefixes=["_","*","`","~","|","_", "**", "***"]

async def missingperms(ctx, permname: str):
    embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs jogod a parancs használatához!\nSzükséges jog: `{permname}`", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=f"Hiba")
    return embed

@client.command(aliases=["setprefix", "prefix", "prefixbeallit", "customprefix"], usage=",setprefix [prefix]")
async def changeprefix(ctx, *, prefix):
    if ctx.author.guild_permissions.administrator:
        for a in disabled_prefixes:
            if a in prefix:
                embed = discord.Embed(title="Hiba", color=0xFF0000, description="A prefix nem tartalmazhat szövegformázó karakterek!", timestamp=datetime.datetime.utcnow(), footer=f"{ctx.author.name} × Hiba")
                await ctx.reply(embed=embed, mention_author=False)
                return
        cursor = db.cursor()
        cursor.execute(f"UPDATE prefix SET prefix=%s WHERE server_id=%s", (prefix, int(ctx.guild.id)))
        db.commit()
        embed = discord.Embed(title="Egyedi Prefix", color=0xFF9900, description=f"Sikeresen átállítottad a bot prefixét a következőre: {prefix}", timestamp=datetime.datetime.utcnow(), footer=f"{ctx.author.name} × Prefix")
        await ctx.reply(embed=embed, mention_author=False)
    else:
        perm = "Adminisztrátor"
        embed = discord.Embed(title="Hiányzó jogok", description=f"Nincs elegendő jogod a parancs végrehajtásához!\nSzükséges jog: `{perm}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
        return

@client.event
async def on_shard_connect(shard_id):
    print(f"[SHARD {shard_id+1}] Kapcsolódva")

@client.event
async def on_shard_ready(shard_id):
    print(f"[SHARD {shard_id+1}] Készen áll")

@client.event
async def on_shard_disconnect(shard_id):
    print(f"[SHARD {shard_id+1}] Lekapcsolódva")

@client.event
async def on_shard_resumed(shard_id):
    print(f"[SHARD {shard_id+1}] Munkamenet folytatva")

@client.event
async def on_command_error(ctx, error):
    command = client.get_command(str(ctx.message.content).replace(",", ""))
    if isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title="<:radon_x:811191514482212874> Hiányzó jogosultság", description=f"A botnak nincs elegendő jogosultsága!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.CommandOnCooldown):
        cd = round(error.retry_after)
        minutes = str(cd // 60)
        seconds = str(cd % 60)
        #days = str(round((error.retry_after/86400000),2))
        embed = discord.Embed(title="Hiba történt!", description=f"Még nem használhatod ezt a parancsot! Hátralévő idő `{minutes}` perc, `{seconds}` másodperc", color=discord.Colour.orange(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, AttributeError):
        embed = discord.Embed(title="Hiba történt!", description=f"Ismeretlen hiba történt! `{error}`", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="<:radon_x:811191514482212874> Hiba", description=f"Nincs jogod a parancs használatához! Ehhez kell: `{error.missing_perms}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
        embed.set_footer(text="Radon × Hiányzó jog", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed, mention_author=False)
    elif isinstance(error, commands.ChannelNotFound):
        embed = discord.Embed(title="Hiba történt!", description=f"Ez a csatorna nem található!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed)
    elif isinstance(error, commands.EmojiNotFound):
        embed = discord.Embed(title="Hiba történt!", description=f"Ez az emotikon nem található!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.MemberNotFound):
        embed = discord.Embed(title="Hiba történt!", description=f"Ez a felhasználó nem található!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.RoleNotFound):
        embed = discord.Embed(title="Hiba történt!", description=f"Ez a rang nem található!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.UserNotFound):
        embed = discord.Embed(title="Hiba történt!", description=f"Ez a felhasználó nem található!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, discord.Forbidden):
        embed = discord.Embed(title="Hiba történt!", description=f"Nincs elegendő jogom ezt a felhasználót kezelni!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    else:
        raise error

@client.event
async def on_ready():
    for x in client.commands:
        a.append(x)
    DiscordComponents(client)
    print(f"====================================================================")
    members = client.get_all_members
    await presence_change.start()
    print(f"{client.user.name} elindult {len(client.guilds)} szerveren, {members} felhasználóval, {len(client.commands)} paranccsal!")
    print("Ha nem muszáj, ne restartolj, csak reloadold a változtatott fájlt!")
    
@tasks.loop(seconds=10)
async def presence_change():
    x = random.choice(a)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.custom,state="asd"))

@client.command(usage=",reload [fájl]")
async def reload(ctx, extension):
    if ctx.message.author.id == 406137394228625419 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 609764483229024297 or ctx.author.id == 360425736688893954:
        try:
            client.reload_extension(f"cogs.{extension}")
            embed = discord.Embed(title="Újratöltés", description=f"`{extension}` újratöltve!", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Hiba!", description="Ez a modul nem található!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
    else:
        embed = discord.Embed(title="<:radon_x:811191514482212874> Hiba", description="Nincs jogod a parancs használatához!", color=discord.Color.orange(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)

@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == 406137394228625419 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 609764483229024297 or ctx.author.id == 360425736688893954:
        try:
            client.unload_extension(f"cogs.{extension}")
            embed = discord.Embed(title="Kikapcsolás", description=f"`{extension}` kikapcsolva!", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Hiba!", description="Ez a modul nem található!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
    else:
        embed = discord.Embed(title="<:radon_x:811191514482212874> Hiba", description="Nincs jogod a parancs használatához!", color=discord.Color.orange(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)

@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == 406137394228625419 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 609764483229024297 or ctx.author.id == 360425736688893954:
        try:
            client.load_extension(f"cogs.{extension}")
            embed = discord.Embed(title="Bekapcsolás", description=f"`{extension}` bekapcsolva!", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except commands.ExtensionNotFound:
            embed = discord.Embed(title="Hiba!", description="Ez a modul nem található!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except Exception as e:
        #	if e == f"Extension 'cogs.{extension}' is already loaded.":
        #      e=f"Ez a cog ({e}) már be van töltve. Használd a ,reload {e} parancsot!"
            embed=discord.Embed(title="Hiba!", description="```{}```".format(e), timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            await ctx.reply(embed=embed, mention_author=False)

@client.command()
async def restart(ctx):
    if ctx.message.author.id == 406137394228625419 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 609764483229024297 or ctx.author.id == 360425736688893954:
        await ctx.reply("<:radon_toltes:811192219579056158> Újraindítás megkezdése...")
        print("Parancsfájlok kitöltése...")
        asd = await ctx.reply("```Parancsfájlok kitöltése...```", mention_author=False)
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                client.unload_extension(f"cogs.{filename[:-3]}")
        print("MySQL kapcsolat bezárása...")
        await asd.edit(content="```Parancsfájlok kitöltése...\nMySQL kapcsolat bezárása...```")
        db.close()
        print("Kijelentkezés...")
        await asd.edit(content="```Parancsfájlok kitöltése...\nMySQL kapcsolat bezárása...\nKijelentkezés...```")
        await client.logout()
        sys.exit()
for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):

                client.load_extension(f"cogs.{filename[:-3]}")
                print(f"----------------------------\n{x}. | Parancsfájl betöltve!")
"""async def setup():
    x = 1
    
                x = x +1
    try: 
        await client.connect(reconnect=True)
    except GatewayNotFound:
        print("Nem sikerült kapcsolódni a Discordhoz!")
        sys.exit()
    except ConnectionClosed:
        print("Kapcsolat bezárult, újracsatlakozás...")
    await client.login(token="", bot=True)
    await client.start()
        
    


loop = asyncio.new_event_loop()
loop.run_until_complete(setup())
loop.stop()
loop.close()"""
schedule.every(5).minutes.do(task)
client.run("ODM4ODM1MzA1MzQyNTY2NDQw.YJA4QQ.oydGffbJWUOoFUZkpXsZ5e_Yqqw")
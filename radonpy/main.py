import asyncio
from asyncio.events import AbstractEventLoop
import discord
from discord.errors import ConnectionClosed, GatewayNotFound
from discord.ext import commands
from discord_components import DiscordComponents
import os
import datetime
import random
import pickle
import mysql.connector as myc
import schedule
from discord.ext import tasks
from discord_slash import SlashCommand
import sys
import logging
import nest_asyncio
import itertools
nest_asyncio.apply()

a = []
mem = 0

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))
logger.addHandler(handler)
logger.info(logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s'))

def setColor(bg, txt):
    os.system(f'setterm -background {bg} -foreground {txt}')

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

intents = discord.Intents()
intents.members=True
intents.guilds=True
intents.typing=True
intents.voice_states=True
intents.messages = True
intents.bans = True
intents.dm_messages = True
intents.reactions = True


client = commands.AutoShardedBot(shard_count=4, command_prefix=(get_prefix), case_insensitive=True, intents=intents)
slash = SlashCommand(client, override_type = True, sync_commands=True)
client.remove_command("help")

blacklist = [ ]
x = 1
disabled_prefixes=["_ _","* *","` `","~~ ~~","||","__ __", "** **", "*** ***"]

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
    setColor('default', 'yellow')
    print(f"[SHARD] ~> {shard_id + 1}. shard kapcsolódva\n")
    setColor('default', 'white')

@client.event
async def on_shard_ready(shard_id):
    setColor('default', 'green')
    print(f"[SHARD] ~> {shard_id + 1}. shard készen áll\n")
    setColor('default', 'white')

@client.event
async def on_shard_disconnect(shard_id):
    setColor('default', 'red')
    print(f"[SHARD] ~> {shard_id + 1}. shard lekapcsolódva\n")
    setColor('default', 'white')

@client.event
async def on_shard_resumed(shard_id):
    setColor('default', 'yellow')
    print(f"[SHARD] ~> {shard_id + 1}. shard munkamenete folytatva\n")
    setColor('default', 'white')

@client.event
async def on_command_error(ctx, error):
    command = client.get_command(str(ctx.message.content).replace(",", ""))
    if isinstance(error, commands.MissingRequiredArgument):
        if command.usage == None: command.usage = "Nincs használat megadva."
        embed = discord.Embed(title="<:radon_x:856423841667743804> Helytelen használat!", description=f"`Használat: {command.usage}`", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.BotMissingPermissions):
        embed = discord.Embed(title="<:radon_x:856423841667743804> Hiányzó jogosultság", description=f"A botnak nincs elegendő jogosultsága!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)
    elif isinstance(error, commands.BadArgument):
        if command.usage == None: command.usage = "Nincs használat megadva."
        embed = discord.Embed(title="<:radon_x:856423841667743804> Helytelen használat!", description=f"`Használat: {command.usage}`", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
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
        embed = discord.Embed(title="<:radon_x:856423841667743804> Hiba", description=f"Nincs jogod a parancs használatához! Ehhez kell: `{error.missing_perms}`", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
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
    elif isinstance(error, discord.errors.Forbidden):
        embed = discord.Embed(title="Hiba történt!", description=f"Nincs elegendő jogom ezt a felhasználót kezelni!", color=discord.Colour.red(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)     

    else:
        raise error
for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try: client.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e: 
                print(f"Hiba történt!\n{e}")
@client.event
async def on_ready():
    #await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.competing, name=f"https://gamersawards.kortdex.hu"))
    #await setup()
    await presence_change.start()
    DiscordComponents(client)
    members = 0
    setColor('default', 'green')
    print(f"[INFO] ~> {client.user.name} elindult {len(client.guilds)} szerveren, {members} felhasználóval, {len(client.commands)} paranccsal!\n")
    setColor('default', 'white')

    
import sys

async def setup():
    print("[INFO] ~> Parancsfájlok betöltése")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try: client.load_extension(f"cogs.{filename[:-3]}")
            except Exception as e: 
                print(f"Hiba történt!\n{e}")
                sys.exit()
    print("[INFO] ~> Parancsfájlok betöltve")
    print("[INFO] ~> Parancs cooldownok betöltése...")
    if os.path.exists("cooldown.pkl"): 
        with open("cooldown.pkl", 'rb') as f:
            d = pickle.load(f)
            for cmd in list(client.commands):
                if cmd.name in d:
                    cmd._buckets = d[cmd.name]
    print("[INFO] ~> Parancs cooldownok betöltve!")
    print("[MYSQL] ~> MYSQL kapcsolódás...")
    db = myc.connect(host="localhost", user="root",
    password="OPiutkmcfjue487ik5",
    db="db")
    print("[MYSQL] ~> Kapcsolódás sikeres!")
    DiscordComponents(client)
    members = 0
    setColor('default', 'green')
    await presence_change.start()
    print(f"[INFO] ~> {client.user.name} elindult {len(client.guilds)} szerveren, {members} felhasználóval, {len(client.commands)} paranccsal!\n")
    setColor('default', 'white')
    
@tasks.loop(seconds=20)
async def presence_change():
    x = random.choice(list(client.commands))
    await client.change_presence(activity=discord.Game(name=f"{len(client.guilds)} szerver » ,{x}"))
    setColor("default", "green")
    print(f"[INFO] ~> A státusz frissült: {len(client.guilds)} szerver » ,{x}\n")
    setColor("default", "white")

@client.command(usage=",reload [fájl]")
async def reload(ctx, extension):
    if ctx.message.author.id == 646073045013889044 or ctx.author.id == 365922646916857865 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 609764483229024297 or ctx.author.id == 654721418273226793 :
        try:
            client.reload_extension(f"cogs.{extension}")
            embed = discord.Embed(title="Újratöltés", description=f"`{extension}` újratöltve!", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Hiba!", description="Ez a modul nem található!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
    else:
        embed = discord.Embed(title="<:radon_x:856423841667743804> Hiba", description="Nincs jogod a parancs használatához!", color=discord.Color.orange(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)

@client.command()
async def unload(ctx, extension):
    if ctx.message.author.id == 646073045013889044 or ctx.author.id == 365922646916857865 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 609764483229024297 or ctx.author.id == 654721418273226793 :
        try:
            client.unload_extension(f"cogs.{extension}")
            embed = discord.Embed(title="Kikapcsolás", description=f"`{extension}` kikapcsolva!", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except:
            embed = discord.Embed(title="Hiba!", description="Ez a modul nem található!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
    else:
        embed = discord.Embed(title="<:radon_x:856423841667743804> Hiba", description="Nincs jogod a parancs használatához!", color=discord.Color.orange(), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed, mention_author=False)

@client.command()
async def load(ctx, extension):
    if ctx.message.author.id == 646073045013889044 or ctx.author.id == 654721418273226793 or ctx.author.id == 365922646916857865 or ctx.author.id == 648168353453572117 or ctx.author.id == 654721418273226793 or ctx.author.id == 609764483229024297 :
        try:
            client.load_extension(f"cogs.{extension}")
            embed = discord.Embed(title="Bekapcsolás", description=f"`{extension}` bekapcsolva!", color=discord.Color.green(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except commands.ExtensionNotFound:
            embed = discord.Embed(title="Hiba!", description="Ez a modul nem található!", color=discord.Color.red(), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed, mention_author=False)
        except Exception as e:
            e=f"Ez a cog ({e}) már be van töltve. Használd a ,reload {e} parancsot!" if e == f"Extension 'cogs.{extension}' is already loaded." else e
            embed=discord.Embed(title="Hiba!", description="```{}```".format(e), timestamp=datetime.datetime.utcnow(), color=discord.Color.red())
            await ctx.reply(embed=embed, mention_author=False)

@client.command()
async def shutdown(ctx):
    if ctx.message.author.id == 646073045013889044 or ctx.author.id == 365922646916857865 or ctx.author.id == 654721418273226793 or ctx.author.id == 648168353453572117 or ctx.author.id == 609764483229024297 :
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
        

"""async def setup():
    x = 1
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):

            client.load_extension(f"cogs.{filename[:-3]}")
            setColor('default', 'blue')
            print(f"[COGS] ~> {x}. parancsfájl betöltve\n ")
            setColor('default', 'white')
            x = x +1
    try: 
        await client.connect(reconnect=True)
    except GatewayNotFound:
        print("Nem sikerült kapcsolódni a Discordhoz!")
        sys.exit()
    except ConnectionClosed:
        print("Kapcsolat bezárult, újracsatlakozás...")
    await client.login("NzEzMDE0NjAyODkxMjY0MDUx.XsZ8mA.35OG8594FoE3sK0r3cyMTKq4HFg")
    await client.start()
    while True:
        try:
            await asyncio.sleep(1)
        except KeyboardInterrupt:
            for filename inghghghghg os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f"cogs.{filename[:-3]}")
            print("MySQL kapcsolat bezárása...")
            db.close()
            print("Kijelentkezés...")
            await client.logout()
            sys.exit()
        
        
    

loop = asyncio.new_event_loop()
loop.run_until_complete(setup())"""

schedule.every(5).minutes.do(task)
client.run("NzEzMDE0NjAyODkxMjY0MDUx.XsZ8mA.UDSc2dTj_dmsZWj3Ul1vb3_32_I")
 

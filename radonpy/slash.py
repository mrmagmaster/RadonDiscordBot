import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import datetime
import random
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_commands import create_choice
import mysql.connector as myc

client = discord.Client()
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print("===================================")
    print("Radon SlashCommands Bot elindult!")
    print("===================================")
    for a in client.guilds:
        guild_ids.append(a)

dbconfig = {
    "host": "95.138.193.29",
    "user": "radonbot",
    "password": "adminroot10",
    "db": "db"
}

db = myc.connect(pool_name="radon2",
                pool_size=16,
                pool_reset_session=True,
                **dbconfig)

guild_ids = []

@slash.slash(name="prefix", description="Prefix visszaállítása az alap prefixre", guild_ids=guild_ids, options=[
    create_option(name="option", description="Válaszd ki hogy megnézni, vagy visszaállítani szeretnéd e a prefixet", option_type=3, required=True, choices=[
        create_choice(name="show", value="show"),
        create_choice(name="reset", value="reset")]
        )
    ]
)
async def test(ctx, option: str):
    if option == "show":
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `prefix` WHERE server_id={int(ctx.guild.id)}")
        result = cursor.fetchall()
        if len(result) == 0:
            default_prefix = ","
            cursor = db.cursor()
            cursor.execute("INSERT INTO prefix (server_id, prefix) VALUES (%s, %s)", (int(ctx.guild.id), default_prefix))
            db.commit()
            prefix_now = default_prefix
            await ctx.send(f"A bot jelenlegi prefixe: {prefix_now}")
        else:
            prefix_now = result[0][1]
            await ctx.send(f"A bot jelenlegi prefixe: {prefix_now}")
    elif option == "reset":
        if ctx.author.guild_permissions.administrator:
            cursor = db.cursor()
            cursor.execute(f"SELECT * FROM `prefix` WHERE server_id={int(ctx.guild.id)}")
            result = cursor.fetchall()
            if len(result) == 0:
                await ctx.send("<:radon_x:811191514482212874> A prefix a szerveren nem lett megváltoztatva, így nem tudom visszaállítani az alapra!")
            else:
                default_prefix = ","
                cursor = db.cursor()
                cursor.execute(f"UPDATE prefix SET prefix=%s WHERE server_id=%s", (default_prefix, int(ctx.guild.id)))
                db.commit()
                await ctx.send("<:radon_pipa:811191514369753149> Sikeresen visszaállítottad a bot prefixét az alap prefixre!")
        else:
            await ctx.send("<:radon_x:811191514482212874> Nincs jogod a parancs használatához!")
    else:
        cursor = db.cursor()
        cursor.execute(f"SELECT * FROM `prefix` WHERE server_id={int(ctx.guild.id)}")
        result = cursor.fetchall()
        if len(result) == 0:
            default_prefix = ","
            cursor = db.cursor()
            cursor.execute("INSERT INTO prefix (server_id, prefix) VALUES (%s, %s)", (int(ctx.guild.id), default_prefix))
            db.commit()
            prefix_now = default_prefix
            await ctx.send(f"A bot jelenlegi prefixe: {prefix_now}")
        else:
            prefix_now = result[0][1]
            await ctx.send(f"A bot jelenlegi prefixe: {prefix_now}")

@slash.slash(name="ping", description="A bot pingjének megtekintése", guild_ids=guild_ids)
async def _ping(ctx):
    await ctx.send(f":ping_pong: Pong! {self.client.latency*1000}ms")


client.run("NzEzMDE0NjAyODkxMjY0MDUx.XsZ8mA.uMjfeQH9fWW99JSXeBuSd5rPZ1c")
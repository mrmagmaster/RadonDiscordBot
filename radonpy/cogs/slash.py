import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import datetime
import random
from discord_slash import SlashCommand
from discord_slash.model import SlashCommandOptionType
import mysql.connector as myc
import mysql.connector as myc
from main import db
from main import slash
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_commands import create_choice

guild_ids = []

class Slash(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        for a in self.client.guilds:
            guild_ids.append(a)

    @slash.slash(name="prefix", description="Prefix megtekintése vagy visszaállítása", guild_ids=guild_ids, options=[
        create_option(name="option", description="Válaszd ki hogy megnézni(show), vagy visszaállítani(reset) szeretnéd e a prefixet", option_type=3, required=True, choices=[
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

def setup(client):
    client.add_cog(Slash(client))
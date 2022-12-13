import discord
from discord_slash import SlashCommand # Importing the newly installed library.

client = discord.Client(intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

@client.event
async def on_ready():
    print("Ready!")

guild_ids = [819154278161448993] # Put your server ID in this array.

@slash.slash(name="ping", guild_ids=guild_ids)
async def _ping(ctx): # Defines a new "context" (ctx) command called "ping."
    await ctx.send(f"Pong! ({client.latency*1000}ms)")

@slash.slash(name="profilkepem", guild_ids=guild_ids)
async def _avatar(ctx):

    embed = discord.Embed(
        title=f"{ctx.author.display_name} profilképe",
        color=discord.Color.teal()
    ).set_image(url=ctx.author.avatar_url)

    await ctx.send(embed=embed)

@slash.slash(name="szia", guild_ids=guild_ids)
async def _helo(ctx):
    await ctx.send("helo")

client.run("ODI0MzM2MTMxOTE4MTM1MzM2.YFt42Q.Uvu6Ufv5JkSXKXDr-AZgkW6AFxw")
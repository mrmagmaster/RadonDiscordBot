import asyncio
import discord
from discord.ext import commands
import datetime
import inspect

client = commands.Bot(command_prefix="!,")

@client.event
async def on_ready():
    print("ok asd")
print()
@client.command()
async def leave(ctx, *, szam):
    if ctx.author.id == 609764483229024297 or ctx.author.id == 406137394228625419 or ctx.author.id == 654721418273226793:
        await ctx.send("Kérlek várj...")
        asd = 0
        for guild in client.guilds:
            try:
                if len(guild.members) < int(szam):
                    await guild.owner.send(f"Kiléptem a(z) {guild.name} szerveredről mert {szam} tag alatti. További infók a support szerveren: https://discord.gg/QGnNVQk8Xs, valamint a weboldalon: https://radonbot.hu")
                    await guild.leave()
                    asd = asd + 1
                    await asyncio.sleep(2)
                else:
                    continue
            except:
                continue
        await ctx.send(f"Kiléptem a(z) {asd} szerverről")

# @client.command(usage=[",eval [parancs]"])
# async def eval(ctx, *, command):
#     if ctx.message.author.id == 406137394228625419 or 654721418273226793 or 609764483229024297 or 648168353453572117 or 751133665492336791:
#         res = eval(command)
#         if inspect.isawaitable(res):
#             await ctx.send(await res)
#         else:
#             await ctx.send(res)

@client.command()
async def serverlist(ctx):
    if ctx.author.id == 609764483229024297 or ctx.author.id == 406137394228625419 or ctx.author.id == 654721418273226793:
        for guild in client.guilds:
            print(f"{guild.name} ({len(guild.members)})")
        await ctx.message.delete()

client.run("NzEzMDE0NjAyODkxMjY0MDUx.XsZ8mA.3V5CSO89WmT7d7TIL3lmFdAhpkg")

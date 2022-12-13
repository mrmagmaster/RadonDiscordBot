import discord
from discord.ext import commands, tasks
import datetime
import random
import aiohttp
import platform
import os
import psutil
import urllib
import io
from contextlib import redirect_stdout
import textwrap
import traceback
import asyncio
import requests

class API(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["porn", "pornó", "porno", "sex", "szex"], usage=",nsfw [4k/hentai/anal/ass/pussy/boobs]")
    async def nsfw(self, ctx, typE=None):
        if ctx.channel.is_nsfw():
            embed = discord.Embed(color=0xFF9900, timestamp=datetime.datetime.utcnow()) 
            embed.set_author(name=f"NSFW × {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar_url)   
            async with aiohttp.ClientSession() as cs:
                if typE == "4k":
                    async with cs.get('https://nekobot.xyz/api/image?type=4k') as r:
                        res = await r.json()
                        embed.set_image(url=res["message"])
                        await ctx.reply(embed=embed, mention_author=False)
                elif typE == "hentai":
                    async with cs.get('https://nekobot.xyz/api/image?type=hentai') as r:
                        res = await r.json()
                        embed.set_image(url=res["message"])
                        await ctx.reply(embed=embed, mention_author=False)
                elif typE == "anal" or typE == "anál":
                    async with cs.get('https://nekobot.xyz/api/image?type=anal') as r:
                        res = await r.json()
                        embed.set_image(url=res["message"])
                        await ctx.reply(embed=embed, mention_author=False)
                elif typE == "segg" or typE == "ass":
                    async with cs.get('https://nekobot.xyz/api/image?type=ass') as r:
                        res = await r.json()
                        embed.set_image(url=res["message"])
                        await ctx.reply(embed=embed, mention_author=False)
                elif typE == "pussy" or typE == "puni" or typE == "vagina":
                    async with cs.get('https://nekobot.xyz/api/image?type=pussy') as r:
                        res = await r.json()
                        embed.set_image(url=res["message"])
                        await ctx.reply(embed=embed, mention_author=False)
                elif typE in ("boobs", "csöcsök", "csöcs", "csocsok", "csocs", "csöcsok", "csocsök", "mell", "tits"):
                    async with cs.get('https://nekobot.xyz/api/image?type=boobs') as r:
                        res = await r.json()
                        embed.set_image(url=res["message"])
                        await ctx.reply(embed=embed, mention_author=False)
                else:
                    await ctx.reply("""Hibás kategória! Elérhető kategóriák:
                                    > 4k
                                    > hentai
                                    > anal
                                    > ass
                                    > pussy
                                    > boobs""")
        else:
            await ctx.reply("Ez nem NSFW csatorna.", mention_author=False)

    @commands.command(aliases=["dog", "puppy", "kutyus"])
    async def kutya(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as r:
                if r.status == 200:
                    js = await r.json()
                embed = discord.Embed(color=0xFF9900)
                embed.set_image(url=js["message"])
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["kacsák", "kacsa", "ducks", "kacsak"])
    async def duck(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://random-d.uk/api/random') as r:
                if r.status == 200:
                    js = await r.json()
                embed = discord.Embed(color=0xFF9900, title="🦆 Kacsák")
                embed.set_image(url=js["url"])
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["rókikák", "róka", "roka", "tyokik", "foxes"])
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://randomfox.ca/floof') as r:
                if r.status == 200:
                    js = await r.json()
                embed = discord.Embed(color=0xFF9900, title="🦊 Rókák")
                embed.set_image(url=js["image"])
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["pandák", "pandas", "pand", "pandak"])
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/img/panda') as r:
                if r.status == 200:
                    js = await r.json()
                embed = discord.Embed(color=0xFF9900, title="🐼 Pandák")
                embed.set_image(url=js["link"])
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["macskák", "cat", "cats", "macskak"])
    async def macska(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/img/cat') as r:
                if r.status == 200:
                    js = await r.json()
                embed = discord.Embed(color=0xFF9900, title="😺 Macskák")
                embed.set_image(url=js["link"])
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["nyul", "nyuszi", "nyulak", "bunnies", "bunnys", "bunnyes", "nyúl"])
    async def bunny(self, ctx):
        async with aiohttp.ClientSession() as cs:
                async with cs.get('https://www.reddit.com/r/Rabbits/new.json?sort=hot') as r:
                    res = await r.json()
                    embed=discord.Embed(color=0xff9900, title="🐇 Nyuszik")
                    embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
                    await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["koalak", "koalas", "koalák"])
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/img/koala') as r:
                if r.status == 200:
                    js = await r.json()
                embed = discord.Embed(color=0xFF9900, title="🐨 Koalák")
                embed.set_image(url=js["link"])
                await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["megölel", "megolel"], usage=",hug [@felhasználó]")
    async def hug(self, ctx, member:discord.Member=None):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://some-random-api.ml/animu/hug') as r:
                if r.status == 200:
                    js = await r.json()
                if member:
                    embed=discord.Embed(color=0xFF9900, title="🤗 Ölelés", description=f"{ctx.author.mention} megölelte {member.mention}-t!")
                    embed.set_image(url=js["link"])
                    await ctx.reply(embed=embed, mention_author=False)
                else:
                    await ctx.reply(content="Meg akarod magad ölelni? Aww...", mention_author=False)

    @commands.command(aliases=["buzikép", "prideimg"], usage=",gaypic (@felhasználó)")
    async def gaypic(self, ctx, member: discord.Member=None):
        if member == None: member = ctx.author
        if ".webp" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".webp", "")
        elif ".gif" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".gif", "")
        result = f"https://some-random-api.ml/canvas/gay/?avatar={avatar_url}"
        embed = discord.Embed(color=0xFF9900, title="🏳‍🌈 Meleg kép")
        embed.set_image(url=result)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["trigger"], usage=",triggered (@felhasználó)")
    async def triggered(self, ctx, member:discord.Member=None):
        if member == None: member = ctx.author
        async with aiohttp.ClientSession() as trigSession:
            async with trigSession.get(f'https://some-random-api.ml/canvas/triggered?avatar={member.avatar_url_as(format="png", size=1024)}') as trigImg:
                imageData = io.BytesIO(await trigImg.read())
                await trigSession.close()
                await ctx.reply(file=discord.File(imageData, 'triggered.gif'), mention_author=False)

    @commands.command(aliases=["gtawasted"])
    async def wasted(self, ctx, member:discord.Member=None):
        if member == None: member = ctx.author
        if ".webp" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".webp", "")
        elif ".gif" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".gif", "")
        result = f"https://some-random-api.ml/canvas/wasted/?avatar={avatar_url}"
        embed=discord.Embed(color=0xFF9900, title="🔫 Wasted")
        embed.set_image(url=result)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command()
    async def tweet(self, ctx, *, comment):
        member = ctx.author
        if ".webp" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".webp", "")
        elif ".gif" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".gif", "")
        res = str(comment).replace(" ", "%20")
        result = f"https://some-random-api.ml/canvas/tweet/?avatar={avatar_url}&username={ctx.author.name}&displayname={ctx.author.name}&comment={res}"
        embed=discord.Embed(color=0xFF9900, title="🐦 Tweet")
        embed.set_image(url=result)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["atweet", "advtweet"])
    async def advancedtweet(self, ctx, replies:int, likes:int, retw:int, *, comment):
        member = ctx.author
        if ".webp" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".webp", "")
        elif ".gif" in str(member.avatar_url): avatar_url = str(member.avatar_url).replace(".gif", "")
        res = comment.replace(" ", "%20")
        result = f"https://some-random-api.ml/canvas/tweet/?avatar={avatar_url}&username={ctx.author.name}&displayname={ctx.author.name}&comment={res}&replies={replies}&likes={likes}&retweets={retw}"
        embed=discord.Embed(color=0xFF9900, title="🐦 Tweet")
        embed.set_image(url=result)
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(aliases=["hexviewer"])
    async def colorviewer(self, ctx, hex):
        result = f"https://some-random-api.ml/canvas/colorviewer/?hex={hex}"
        embed=discord.Embed(color=0xFF9900, title="🔴 HEX színnéző")
        embed.set_image(url=result)
        await ctx.reply(embed=embed, mention_author=False)

def setup(client):
    client.add_cog(API(client))
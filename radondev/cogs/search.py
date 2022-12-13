import discord
from discord.ext import commands
import datetime
import random
import asyncio
import aiohttp
import urllib.parse
import io
import bs4
import re

class Search(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ["keresés", "google"], usage=",search <keresendő szöveg>")
    async def search(self, ctx, *, search):
        searchRes = "https://www.google.com/search?q=" + str(search).replace(" ", "+")
        await ctx.send(searchRes)

    @commands.command(aliases = ["pnkeresés", "pn", "pnsearch", "piknód"], usage=",picnode <keresendő szöveg>")
    async def picnode(self, ctx, *, search):
        searchRes = "https://picnode.hu?search=" + str(search).replace(" ", "+")
        await ctx.send(searchRes)

    @commands.command(aliases = ["phkeresés", "ph", "phsearch"], usage=",pornhub <keresendő videó>")
    async def pornhub(self, ctx, *, search):
        if ctx.channel.is_nsfw():
            searchRes = "https://www.pornhub.com/video/search?search=" + str(search).replace(" ", "+")
            await ctx.send(searchRes)
        else:
            await ctx.send("Ez nem nsfw csatorna!")

    @commands.command(aliases = ["twsearch", "twkeresés", "tw"], usage=",twitter <keresendő profil>")
    async def twitter(self, ctx, *, search):
        searchRes = "https://twitter.com/search?q=" + str(search).replace(" ", "+")
        await ctx.send(searchRes)

    @commands.command(aliases = ["twitchsearch", "twitchkeresés"], usage=",twitch <keresendő szöveg>")
    async def twitch(self, ctx, *, search):
        searchRes = "https://twitter.com/search?q=" + str(search).replace(" ", "+")
        await ctx.send(searchRes)

    @commands.command(aliases = ["steamsearch", "stsearch", "st"], usage=",steam <keresendő játék>")
    async def steam(self, ctx, *, search):
        searchRes = "https://store.steampowered.com/search/?term=" + str(search).replace(" ", "+")
        await ctx.send(searchRes)

def setup(client):
    client.add_cog(Search(client))

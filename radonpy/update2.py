import discord
from discord.ext import commands
import datetime
from discord.utils import get
from google_speech import Speech
import asyncio
import aiohttp
import random

class Update(commands.Cog):
    def __init__(self, client):
        self.client = client


        
    @commands.command()
    async def rise(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                channel = ctx.message.author.voice.channel
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `RiseFM` élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://188.165.11.30:8080/'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `RiseFM` élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://188.165.11.30:8080/'))

    

def setup(client):
    client.add_cog(Update(client))

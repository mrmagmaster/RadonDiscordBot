import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get

class Radio(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['radio1', 'rádió1'])
    async def radio11(self, ctx):
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
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `Rádió1` élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://stream2.radio1.hu/high.mp3'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `Rádió1` élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://stream2.radio1.hu/high.mp3'))

    @commands.command(aliases=['petofi'])
    async def petőfi(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `Petőfi` rádió élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://icast.connectmedia.hu/4738/mr2.mp3'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `Petőfi` rádió élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://icast.connectmedia.hu/4738/mr2.mp3'))

    @commands.command(aliases=['retró'])
    async def retro(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send(" > Sikeresen becsatlakoztam a hangcsatornába és a `Retró` rádió élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://myonlineradio.hu/ldblncr/retro-radio/mid.mp3'))
        else:
                await channel.connect()
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> 📻 A **Retró rádió** élőadása hamarosan elindul!")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://myonlineradio.hu/ldblncr/retro-radio/mid.mp3'))

    @commands.command()
    async def sunshine(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> 📻 A **Sunshine** élőadása hamarosan elindul!")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://195.56.193.129:8100/;stream.nsv#.mp3'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("> 📻 A **Sunshine** élőadása hamarosan elindul!")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://195.56.193.129:8100/;stream.nsv#.mp3'))

    @commands.command()
    async def kossuth(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> 📻 A **Kossuth rádió** élőadása hamarosan elindul!")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://icast.connectmedia.hu/4736/mr1.mp3'))
        else:   
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("> 📻 A **Kossuth rádió** élőadása hamarosan elindul!")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('https://icast.connectmedia.hu/4736/mr1.mp3'))

    @commands.command(aliases=['rádió88'])
    async def radio88(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await channel.connect()
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> 📻 A **Radio88** élőadása hamarosan elindul!")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://stream.radio88.hu:8000/;stream.nsv#.mp3'))
        else:
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("> 📻 A **Radio88** élőadása hamarosan elindul!")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://stream.radio88.hu:8000/;stream.nsv#.mp3'))

    @commands.command()
    async def freshfm(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `FreshFM` élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://stream3.virtualisan.net:8000/freshfm.mp3'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("Sikeresen becsatlakoztam a hangcsatornába és a `FreshFM` élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://stream3.virtualisan.net:8000/freshfm.mp3'))

    @commands.command()
    async def radonradio(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `Radon Rádió` élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://radon.v4y.hu:6004/radonradio.ogg'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("Sikeresen becsatlakoztam a hangcsatornába és a `Radon Rádió` élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://radon.v4y.hu:6004/radonradio.ogg'))

    @commands.command()
    async def risefm(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `RiseFM` élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://188.165.11.30:8080/'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("Sikeresen becsatlakoztam a hangcsatornába és a `RiseFM` élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://188.165.11.30:8080/'))

    @commands.command()
    async def radiogaga(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `Radio Gaga` élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://rc.radiogaga.ro:8000/live'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("Sikeresen becsatlakoztam a hangcsatornába és a `Radio Gaga` élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://rc.radiogaga.ro:8000/live'))

    @commands.command()
    async def klubradio(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            if not ctx.author.voice.channel == ctx.voice_client.channel:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xff0000)
                await ctx.send(embed=embed)
                return
            else:
                await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
                await ctx.send("> Sikeresen becsatlakoztam a hangcsatornába és a `Klub Rádió` élő közvetítését játszom. 🎵")
                get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://stream.klubradio.hu:8080/bpstream'))
        else:
            await channel.connect()
            await ctx.guild.change_voice_state(channel=channel, self_mute=False, self_deaf=True)
            await ctx.send("Sikeresen becsatlakoztam a hangcsatornába és a `Klub rádió` élő közvetítését játszom. 🎵")
            get(self.client.voice_clients, guild=ctx.guild).play(FFmpegPCMAudio('http://stream.klubradio.hu:8080/bpstream'))

def setup(client):
    client.add_cog(Radio(client))
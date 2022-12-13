import discord
from discord.ext import commands
import datetime
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from gtts import gTTS


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        embed = discord.Embed(description=f"`{data['title']}` hozzáadva a lejátszási listához! <:radon_check:856423841612824607>", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Zene hozzáadás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Zene hozzáadás", icon_url="https://cdn.discordapp.com/avatars/713014602891264051/c9ab2afb5c71f157cc4b5aefd64cc7af.webp?size=1024")
        await ctx.send(embed=embed)
        if download: source = ytdl.prepare_filename(data)
        else: return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']
        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)
        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer(commands.Cog):

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.np = None
        self.volume = .5
        self.current = None
        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()
            try:
                async with timeout(300): source = await self.queue.get()
            except asyncio.TimeoutError: return self.destroy(self._guild)
            if not isinstance(source, YTDLSource):
                try: source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception:
                    embed = discord.Embed(description="Nem sikerült feldolgozni a kért zenét!", color=0xFF0000)
                    embed.set_author(name="Hiba <:radon_x:811191514482212874>", icon_url=self._message.author.avatar_url)
                    embed.set_footer(text=f"{self._message.author.name} × Hiba", icon_url=self.bot.user.avatar_url)
                    await self._channel.send(embed=embed)
                    continue
            source.volume = self.volume
            self.current = source
            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(description=f"Sikeresen elindítottam az alábbi zenét: `{source.title}` | <:radon_check:856423841612824607> ", color=0xFF9900)
            embed.set_author(name="Zene elindítva!", icon_url=self._message.author.avatar_url)
            embed.set_footer(text=f"{self._message.author.name} × Zene", icon_url=self.bot.user.avatar_url)
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()
            source.cleanup()
            self.current = None
            try: await self.np.delete()
            except discord.HTTPException: pass

    def destroy(self, guild): return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try: await guild.voice_client.disconnect()
        except AttributeError: pass
        try: del self.players[guild.id]
        except KeyError: pass

    async def __local_check(self, ctx):
        if not ctx.guild: raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        if isinstance(error, InvalidVoiceChannel):
            await ctx.send("Nem tudtam csatlakozni a hangcsatornába!")
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        try: player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player

    @commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx):
        try: channel = ctx.author.voice.channel
        except AttributeError: await ctx.send("Csatlakozz be egy hangcsatornába, ahova szeretnéd, hogy csatlakozzak!")
        vc = ctx.voice_client
        if vc:
            if vc.channel.id == channel.id: return
            try: await vc.move_to(channel)
            except asyncio.TimeoutError: await ctx.send("Nem tudtam csatlakozni a hangcsatornába!")
        else:
            try: await channel.connect()
            except asyncio.TimeoutError: await ctx.send("Nem tudtam csatlakozni a hangcsatornába!")
        embed = discord.Embed(description=f"Csatlakoztam a hangcsatornádba!", color=0xFF9900, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Csatlakozás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='play')
    async def play_(self, ctx, *, search: str):
        vc = ctx.voice_client
        if not vc: await ctx.invoke(self.connect_)
        player = self.get_player(ctx)
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
        await player.queue.put(source)

    @commands.command(name='pause')
    async def pause_(self, ctx):
        vc = ctx.voice_client 
        if not vc or not vc.is_playing():
            embed = discord.Embed(description="Jelenleg nem játszok le zenét, ezért nem tudok mit szüneteltetni!", color=0xFF0000)
            embed.set_author(name="Hiba", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        elif vc.is_paused(): return 
        vc.pause()
        embed = discord.Embed(description=f"`{ctx.author.name}` szüneteltette a zenét!", color=0xFF9900)
        embed.set_author(name="Megállítás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='resume')
    async def resume_(self, ctx):
        vc = ctx.voice_client 
        if not vc or not vc.is_connected():
            embed = discord.Embed(description="Jelenleg nem játszok le zenét, ezért nem tudom minek folytatni a lejátszását!", color=0xFF0000)
            embed.set_author(name="Folytatás", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return
        elif not vc.is_paused(): return 
        vc.resume()
        embed = discord.Embed(description=f"`{ctx.author.mention}` folytatta a zenét!", color=0xFF9900)
        embed.set_author(name="Folytatás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        return

    @commands.command(name='skip')
    async def skip_(self, ctx):
        vc = ctx.voice_client 
        if not vc or not vc.is_connected():
            embed = discord.Embed(description=f"Jelenleg nem játszok le zenét, ezért nem tudok mit átugrani!", color=0xFF0000)
            embed.set_author(name="Átugrás", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed) 
        if vc.is_paused(): pass
        elif not vc.is_playing(): return 
        vc.stop()
        embed = discord.Embed(description=f"{ctx.author.mention} átugorta a zenét a zenét!", color=0xFF9900)
        embed.set_author(name="Átugrás", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='queue', aliases=['q'])
    async def queue_info(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send("Nem vagyok hangcsatornában!")
            return
        player = self.get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(description=f"A lejátszási lista üres!", color=0xFF0000)
            embed.set_author(name="Lista", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))
        fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
        embed = discord.Embed(description=fmt)
        embed.set_author(name="Lejátszási lista ({})".format(len(upcoming)), icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='now')
    async def now_playing_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send("Nem vagyok hangcsatornában!")
            return
        player = self.get_player(ctx)
        if not player.current:
            await ctx.send("Nem játszok le zenét jelenleg!")
            return
        try: await player.np.delete()
        except discord.HTTPException: pass
        player.np = await ctx.send(f'**Most szól:** `{vc.source.title}\nKérte: `{vc.source.requester}`')

    @commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol: int):
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send("Nem vagyok hangcsatornában!")
            return
        if not 0 < vol < 101:
            embed = discord.Embed(description="Csak 1 és 100 közötti számot írhatsz be!", color=0xFF0000)
            embed.set_author(name="Hangerő", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return
        player = self.get_player(ctx)
        if vc.source:vc.source.volume = vol / 100
        player.volume = vol / 100
        embed = discord.Embed(description=f"{ctx.author.mention} átállította a hangerőt!", color=0xFF9900)
        embed.set_author(name="Hangerő", icon_url=ctx.author.avatar_url)
        embed.set_footer(text=f"{ctx.author.name} × Zene", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        return

    @commands.command(name='stop', aliases=['leave'])
    async def stop_(self, ctx):
        vc = ctx.voice_client
        if not vc or not vc.is_connected(): await ctx.send("Jelenleg nem játszok zenét!")
        await self.cleanup(ctx.guild)

    @commands.command(usage=",voicesay [nyelv(országkód)] [szöveg]", aliases=["vcsay","vsay","vc","audiosay","asay","ausay","speech","felolvas","olvas","felolvasás"])
    async def voicesay(self, ctx, lang, *, txt):
        if len(txt) > 500:
            await ctx.reply("Ez a szöveg túl hosszú!")
            return
        try:
            text2 = str(txt)
            import string
            import random
            soundid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=30))
            speech = gTTS(text=text2, lang=lang, slow=False)
            speech.save(f"/var/www/cdn/sounds/voicesay/{str(soundid)}.mp3")
            vc = ctx.voice_client
            if not vc: await ctx.invoke(self.connect_)
            discord.utils.get(self.bot.voice_clients, guild=ctx.guild).play(discord.FFmpegPCMAudio(f'/var/www/cdn/sounds/voicesay/{str(soundid)}.mp3'))
            embed = discord.Embed(description=f"Sikeresen elindítottam a felolvasást!", color=0xFF9900)
            embed.set_author(name="Voicesay", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Voicesay", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except ValueError:
            embed = discord.Embed(description=f"Ez a nyelv nem támogatott!", color=0xFF9900)
            embed.set_author(name="Voicesay", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Voicesay", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(description=f"Épp felolvasok vagy zenét játszok!", color=0xFF9900)
            embed.set_author(name="Voicesay", icon_url=ctx.author.avatar_url)
            embed.set_footer(text=f"{ctx.author.name} × Voicesay", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Music(client))

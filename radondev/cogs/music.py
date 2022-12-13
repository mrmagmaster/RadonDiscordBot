import discord
from discord.errors import ClientException
from discord.ext import commands
import youtube_dl
from discord.utils import get
import urllib
import re
import asyncio

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.loop = client.loop

    @commands.command()
    async def skip(self, ctx):
        """A jelenlegi zenéket átugorja."""
        state = self.get_state(ctx.guild)
        client = ctx.guild.voice_client
        if ctx.channel.permissions_for(
                ctx.author).administrator or state.is_requester(ctx.author):
            # azonnal kihagyja hogyha adminisztrátor
            client.stop()
        elif self.config["vote_skip"]:
            # szavazás hogy a bot átugorja a zenét
            channel = client.channel
            self._vote_skip(channel, ctx.author)
            # meghírdeti a szavazást
            users_in_channel = len([
                member for member in channel.members if not member.bot
            ])  # ne számoljon botokat
            required_votes = math.ceil(
                self.config["vote_skip_ratio"] * users_in_channel)
            await ctx.send(
                f"{ctx.author.mention} szavazott hogy átugorja ({len(state.skip_votes)}/{required_votes} szavazat)"
            )
        else:
            raise commands.CommandError("Sajnos a szavazás átugrása le van tíltva.")

    def _vote_skip(self, channel, member):
        """Regisztrálj egy `tag` hogy kihagyd a dal lejátszását."""
        logging.info(f"{member.name} szavazott az átugrásra")
        state = self.get_state(channel.guild)
        state.skip_votes.add(member)
        users_in_channel = len([
            member for member in channel.members if not member.bot
        ])  # ne számoljon botokat
        if (float(len(state.skip_votes)) /
                users_in_channel) >= self.config["vote_skip_ratio"]:
            # elég ember szavazott az átugrásra
            logging.info(f"Enough votes, skipping...")
            channel.guild.voice_client.stop()

    def _play_song(self, client, state, song):
        state.now_playing = song
        state.skip_votes = set()  # összes szavazat törlése
        source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(song.stream_url), volume=state.volume)

        def after_playing(err):
            if len(state.playlist) > 0:
                next_song = state.playlist.pop(0)
                self._play_song(client, state, next_song)
            else:
                asyncio.run_coroutine_threadsafe(client.disconnect(),
                                                self.bot.loop)

        client.play(source, after=after_playing)

    @commands.command(usage=",play <cím/url>")
    async def play(self, ctx, *, search):
        global music_loop
        print("[ZENERENDSZER] ~> Előkészülés...")
        print("[YOUTUBE]  ~> Keresés...")
        try:
            query_string = urllib.parse.urlencode({'search_query': search})
            htm_content = urllib.request.urlopen(
                'http://www.youtube.com/results?' + query_string)
            search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
            link = 'http://www.youtube.com/watch?v=' + search_results[0]
        except IndexError:
            print("[YOUTUBE] ~> Keresés meghiusúlt")
            indexerror = discord.Embed(title="<:radon_x:811191514482212874> - Nem találtam meg a zenét.", color=0xFF9900)
            await ctx.send(embed=indexerror)
            return
        try:
            print("[ZENERENDSZER] ~> Csatlakozás folyamatban...")
            voicechannel = ctx.message.author.voice.channel
            voice = get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():
                if not ctx.author.voice.channel == ctx.voice_client.channel:
                    print("[ZENERENDSZER] ~> A bot másik hangcsatornában van")
                    embed = discord.Embed(title="<:radon_x:811191514482212874> - Másik hangcsatornában vagyok!", color=0xFF9900)
                    await ctx.send(embed=embed)
                    return
                else:
                    print("[ZENERENDSZER] ~> Letöltés megkezdése...")
                    ydl_opts = {'format': 'bestaudio',
                    'track': 'title'}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        print("[YOUTUBE] ~> Zene letöltése")
                        info = ydl.extract_info(link, download=False)
                        URL = info['formats'][0]['url']
                        title = info.get('title', None)
                        try:
                            print("[ZENERENDSZER] ~> Lejátszási kísérlet...")
                            get(self.client.voice_clients, guild=ctx.guild).play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                            
                            music_loop = link
                            print("[ZENERENDSZER] ~> Zene elindítva")
                        except ClientException:
                            playEmbed = discord.Embed(title="<:radon_x:811191514482212874> - Jelenleg zenét játszok le", color=0xFF9900)
                            await ctx.send(embed=playEmbed)
                            return
                        playEmbed = discord.Embed(title=":notes: - {}".format(title), color=0xFF9900)
                        await ctx.send(embed=playEmbed)
            else:
                await voicechannel.connect()
                ydl_opts = {'format': 'bestaudio',
                'track': 'title'}
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(link, download=False)
                    URL = info['formats'][0]['url']
                    title = info.get('title', None)
                    try:
                        get(self.client.voice_clients, guild=ctx.guild).play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
                        
                        music_loop = link
                    except ClientException:
                            playEmbed = discord.Embed(title="<:radon_x:811191514482212874> - Jelenleg zenét játszok le", color=0xFF9900)
                            await ctx.send(embed=playEmbed)
                            return
                    playEmbed = discord.Embed(title=":notes: - {}".format(title), color=0xFF9900)
                    await ctx.send(embed=playEmbed)
            await ctx.guild.change_voice_state(channel=voicechannel, self_mute=False, self_deaf=True)
        except AttributeError:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Nem vagy hangcsatornában!", color=0xFF9900)
                await ctx.send(embed=embed)
        except commands.errors.CommandInvokeError:
                embed = discord.Embed(title="<:radon_x:811191514482212874> - Ismeretlen hiba történt", color=0xFF9900)
                await ctx.send(embed=embed)

    @commands.command(aliases=["stop"])
    async def pause(self, ctx):
        a = get(self.client.voice_clients, guild=ctx.guild)
        if a:
            if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
                a.pause()
                music = discord.Embed(title=":notes: - Zene megállítva", color=0xFF9900)
                await ctx.send(embed=music)
            else:
                noMusic = discord.Embed(title="<:radon_x:811191514482212874> - Nem állíthatod meg a zenét!", color=0xFF9900)
                await ctx.send(embed=noMusic)
        else:
            noMusic = discord.Embed(title="<:radon_x:811191514482212874> - Nem található zene", color=0xFF9900)
            await ctx.send(embed=noMusic)



    @commands.command()
    async def resume(self, ctx):
        a = get(self.client.voice_clients, guild=ctx.guild)
        if a:
            if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
                ctx.message.author.voice.channel
                a.resume()
                music = discord.Embed(title=":notes: - Zene elindítva", color=0xFF9900)
                await ctx.send(embed=music)
            else:
                noMusic = discord.Embed(title="<:radon_x:811191514482212874> - Nem állíthatod meg a zenét!", color=0xFF9900)
                await ctx.send(embed=noMusic)
        else:
            noMusic = discord.Embed(title="<:radon_x:811191514482212874> - Nem található zene", color=0xFF9900)
            await ctx.send(embed=noMusic)

    @commands.command()
    async def leave(self, ctx):
        a = get(self.client.voice_clients, guild=ctx.guild)
        if a:
            if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
                ctx.message.author.voice.channel
                await a.disconnect()
                disconnect = discord.Embed(title=":notes: - Lecsatlakoztam a hangcsatornáról", color=0xFF9900)
                await ctx.send(embed=disconnect)
            else:
                ok = discord.Embed(title="<:radon_x:811191514482212874> - Nem csatlakoztathatsz le a hangcsatornáról!", color=0xFF9900)
                await ctx.send(embed=ok)
        else:
            ok = discord.Embed(title="<:radon_x:811191514482212874> - Nem vagyok hangcsatornában!", color=0xFF9900)
            await ctx.send(embed=ok)

    @commands.command(usage=",loop <be/ki>")
    async def loop(self, ctx, option):
        music = music_loop
        voicechannel = ctx.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)
        if option == "be":
            try: task = self.client.loop.create_task(looptask(music=music, voicechannel=voicechannel, client_voice=voice)) 
            except: await ctx.send("A loop már be van kapcsolva vagy nem szól zene")
            await ctx.send("Sikeresen bekapcsoltad az ismétlődést.")
        if option == "ki":
            try: task.cancel()
            except: await ctx.send("A loop már ki van kapcsolva vagy nem szól zene")
            await ctx.send("Sikeresen kikapcsoltad az ismétlődést.")

    """@commands.command()
    async def volume(self, ctx, volume):
        
        a = get(self.client.voice_clients, guild=ctx.guild)
        if a:
            if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
                    discord.PCMVolumeTransformer.volume(volume=float(volume))
                    ok = discord.Embed(title=f":notes: - Hangerő beállítva {volume}%-ra!", color=0xFF9900)
                    await ctx.send(embed=ok) 
            else:
                ok = discord.Embed(title="<:radon_x:811191514482212874> - Nem állíthatsz hangerőt!", color=0xFF9900)
                await ctx.send(embed=ok)
        else:
                ok = discord.Embed(title="<:radon_x:811191514482212874> - Nem csatlakoztathatsz le a hangcsatornáról!", color=0xFF9900)
                await ctx.send(embed=ok)"""

async def looptask(music, voicechannel, client_voice):
    while True:
        while client_voice.is_playing():
            await asyncio.sleep(1)
        try:
            voicechannel
        except:
            client_voice.disconnect()
            break
        ydl_opts = {'format': 'bestaudio',
                    'track': 'title'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        print("[YOUTUBE] ~> Zene letöltése")
                        info = ydl.extract_info(music, download=False)
                        URL = info['formats'][0]['url']
                        client_voice.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))

def setup(client):
    client.add_cog(Music(client))

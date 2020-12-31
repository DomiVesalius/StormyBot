from typing import Dict, List
import discord
from random import choice
from discord.ext import commands
from discord.ext.commands import Context
from embed_maker import enqueue_embed, now_playing_embed
from lib.queue import Queue
from lib.ydl_ffmpeg_opts import YDL_OPTS, FFMPEG_OPTIONS
from lib.audio import Audio
from youtube_search import YoutubeSearch
import youtube_dl
import asyncio


class Music(commands.Cog):
    """
    The Music commands for this discord bot.
    """

    client: discord.ext.commands.bot.Bot
    queues: Dict[discord.voice_client.VoiceClient, Queue]
    greetings: List[str]
    farewells: List[str]

    def __init__(self, client: discord.ext.commands.bot.Bot) -> None:
        """
        Initializes this music Cog
        """
        self.client, self.queues = client, {}
        self.greetings = ["Ay boss!", "Henlo.", 'Pain.']
        self.farewells = ["Aight, I'ma head out", "Sayonara", "oof"]

    @commands.command(name='join', aliases=['Join'])
    async def join(self, ctx: Context,
                   outputs: bool = True) -> None:
        """
        Makes <self> join the voice channel if any.
        :param outputs: If outputs is True, event messages will be sent by the bot.
        :param ctx: Context
        """
        try:  # If the command invoker is in a voice channel
            channel = ctx.message.author.voice.channel
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():  # The bot is already connected to channel
                if outputs:
                    await ctx.send(f"I am already in {channel}")
            else:  # The bot is not connected to any voice channel.
                self.queues[ctx.guild.id] = Queue()
                await channel.connect()
                if outputs:
                    await ctx.send(f"{choice(self.greetings)}\nConnected to {channel}")
        except AttributeError:  # Invoker is not in a voice channel.
            await ctx.send("You need to be in a voice channel for me to join..")

    @commands.command(name='leave', aliases=['Leave', 'Stop', 'stop'])
    async def leave(self, ctx: Context) -> None:
        """
        Makes the bot leave the voice channel it is in if any.
        :param ctx: Context
        """
        server = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        try:
            user_channel = ctx.author.voice.channel
            if user_channel != server.channel:  # If the user isn't in the same vc as self
                await ctx.send("You need to be in the same voice channel as me.")
                return None
            server.stop()
            await server.disconnect()
            await ctx.send(choice(self.farewells))
            if self.queues.get(ctx.guild.id):  # Removing the servers queue
                del self.queues[ctx.guild.id]
        except AttributeError:
            await ctx.send("I am not in any voice channel.")

    @commands.command(name="pause", aliases=["unpause", "up", "resume"])
    async def pause(self, ctx: Context) -> None:
        """
        If the bot is connected to a voice channel, pauses its audio if any is playing,
        and resumes audio if it is paused.
        """
        try:  # Checking if the command invoker is in a voice channel
            author_vc = ctx.message.author.voice.channel.id
        except AttributeError:
            await ctx.send("You need to be in the same voice channel as me.")
            return None

        voice_client = ctx.voice_client
        # Checking if invokers vc is the same as bots vc
        if voice_client.channel.id != author_vc:
            await ctx.send("You need to be in the same voice channel as me.")
            return None

        if not voice_client.is_connected():
            await ctx.send("I'm not in any voice channels.")
            return
        if voice_client.is_playing():
            voice_client.pause()
            embed = discord.Embed(title="Music playback has been paused")
        else:
            voice_client.resume()
            embed = discord.Embed(title="Music playback has resumed.")
        await ctx.send(embed=embed)

    @commands.command(name='play', aliases=['Play'])
    async def play(self, ctx: Context, *, query: str) -> None:
        """
        Plays the audio of the given query if found.
        """
        try:  # Checking if the command invoker is in a voice channel
            author_vc = ctx.message.author.voice.channel.id
        except AttributeError:
            await ctx.send("You need to be in the same voice channel as me.")
            return None

        await self.join(ctx, outputs=False)

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.channel.id != author_vc:
            await ctx.send("You need to be in the same voice channel as me.")
            return None

        results = youtube_search(query, 1)

        if not results:
            await ctx.send(f"Could not find any youtube video relating to {query}")
            return None
        else:
            results = results[0]

        video_link = f"https://www.youtube.com{results['url_suffix']}"
        with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
            info = ydl.extract_info(video_link, download=False)
            audio_url = info['formats'][0]['url']

        results['audio_link'], results['video_link'] = audio_url, video_link
        new_audio = Audio(results)

        server_queue = self.queues.get(ctx.guild.id)
        in_use = voice.is_playing() or voice.is_paused() or not server_queue.is_empty()
        if in_use:  # There are other songs in the queue
            server_queue.enqueue(new_audio)  # Queue next song and return
            await ctx.send(embed=enqueue_embed(new_audio, ctx.author.mention))
            return None

        server_queue.enqueue(new_audio)  # Queuing first song in the queue
        await ctx.send(embed=enqueue_embed(new_audio, ctx.author.mention))

        next_audio = server_queue.dequeue()
        audio_src = discord.FFmpegPCMAudio(next_audio.audio_url, **FFMPEG_OPTIONS)
        voice.play(audio_src, after=lambda x: self.play_next(ctx))
        await ctx.send(embed=now_playing_embed(next_audio, ctx.author.mention))

    def play_next(self, ctx: Context) -> None:
        """
        Play the next song in the queue.
        """
        server_queue = self.queues.get(ctx.guild.id)
        if server_queue is None:  # server has no queue
            return None
        if not server_queue.is_empty():  # Playing next song only if there is one.
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            next_source = server_queue.dequeue()
            try:
                voice.play(discord.FFmpegPCMAudio(next_source.audio_url,
                                                  **FFMPEG_OPTIONS),
                           after=lambda x: self.play_next(ctx))  # Playing audio
                asyncio.run_coroutine_threadsafe(ctx.send(embed=now_playing_embed(
                    next_source, ctx.author.mention)), self.client.loop)
            except AttributeError:
                pass

    @commands.command(name="skip", aliases=["Skip", "next", "Next"])
    async def skip(self, ctx: Context) -> None:
        """
        Skips the currently playing song.
        """
        try:  # Checks if the command author is in a voice channel

            author_vc = ctx.message.author.voice.channel.id
            bot_vc = discord.utils.get(self.client.voice_clients,
                                       guild=ctx.guild).channel.id
            if bot_vc == author_vc:
                try:
                    if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                        ctx.voice_client.stop()
                        await ctx.send("⏩ Skipped")
                    else:
                        await ctx.send("I'm not playing anything right now.")
                except AttributeError:
                    await ctx.send("I'm not in a voice channel atm.")

        except AttributeError:  # If command author isn't in voice channel, does nothing.
            pass

    @commands.command(name='loop', aliases=['Loop'])
    async def loop(self, ctx: Context) -> None:
        """
        Sets the queue to looping.
        """
        server_queue = self.queues.get(ctx.guild.id)

        try:
            server_queue.loop()
            if server_queue.is_looping():
                await ctx.send("🔁 Now looping...")
            else:
                await ctx.send("➡ Queue is no longer looping...")
        except AttributeError:  # There is no active queue for this server
            pass

    @commands.command(name='queue', aliases=["q", "Q", "Queue"])
    async def queue(self, ctx: Context) -> None:
        """
        Displays the list of items in the queue.
        """
        server_queue = self.queues.get(ctx.guild.id)

        try:
            str_list = server_queue.string_formatted()

            if not str_list:
                description = "```EMPTY```"
            else:
                description = f"```python\n{str_list}\n```"
            queue_embed = discord.Embed(title="Current Queue",
                                        description=description)
            await ctx.send(embed=queue_embed)
        except AttributeError:  # server_queue may be None
            await ctx.send("There is no queue, take off your clothes 👀")


def setup(client: discord.ext.commands.bot.Bot) -> None:
    """
    Loads the Music cog.
    """
    client.add_cog(Music(client))


def youtube_search(query: str, max_results: int = 1) -> list:
    """
    Returns a list of video results given a search term <query>
    :param max_results: The number of results to return.
    :param query: The video you are looking for.
    :return:
    """
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    return results

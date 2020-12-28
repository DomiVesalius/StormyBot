import discord
import youtube_dl
from random import choice
from discord.ext import commands
from lib.queue import Queue


class Music(commands.Cog):
    """
    The Music commands for this discord bot.
    """

    client: discord.ext.commands.bot.Bot
    queue: Queue

    def __init__(self, client: discord.ext.commands.bot.Bot) -> None:
        """
        Initializes this music Cog
        """
        self.client, self.queue = client, Queue()
        self.greetings = ["Ay boss!", "Henlo.", 'Pain.']
        self.farewells = ["Aight, I'ma head out", "Sayonara", "oof"]

    @commands.command(name='join', aliases=['Join'])
    async def join(self, ctx: discord.ext.commands.context.Context,
                   outputs: bool = True) -> None:
        """
        Makes <self> join the voice channel if any.
        :param outputs: If outputs is True, event messages will be sent by the bot.
        :param ctx: discord.ext.commands.context.Context
        """
        try:  # If the command invoker is in a voice channel
            channel = ctx.message.author.voice.channel
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():  # The bot is already connected to channel
                if outputs:
                    await ctx.send(f"I am already in {channel}")
            else:  # The bot is not connected to any voice channel.
                await channel.connect()
                if outputs:
                    await ctx.send(f"{choice(self.greetings)}\nConnected to {channel}")
        except AttributeError:  # Invoker is not in a voice channel.
            await ctx.send("You need to be in a voice channel for me to join..")

    @commands.command(name='leave', aliases=['Leave'])
    async def leave(self, ctx: discord.ext.commands.context.Context) -> None:
        """
        Makes the bot leave the voice channel it is in if any.
        :param ctx: discord.ext.commands.context.Context
        """
        server = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        try:
            user_channel = ctx.author.voice.channel
            if user_channel != server.channel:  # If the user isn't in the same vc as self
                await ctx.send("You need to be in the same voice channel as me.")
                return None
            await server.disconnect()
            await ctx.send(choice(self.farewells))
        except AttributeError:
            await ctx.send("I am not in any voice channel.")


def setup(client: discord.ext.commands.bot.Bot) -> None:
    """
    Loads the Music cog.
    """
    client.add_cog(Music(client))

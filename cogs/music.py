import discord
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

    @commands.command(name='join', aliases=['Join'])
    async def join(self, ctx) -> None:
        """
        Makes <self> join the voice channel if any.
        :param ctx: discord.ext.commands.context.Context
        """
        try:  # If the command invoker is in a voice channel
            channel = ctx.message.author.voice.channel
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            if voice and voice.is_connected():  # The bot is already connected to channel
                await ctx.send(f"I am already in {channel}")
            else:  # The bot is not connected to any voice channel.
                await channel.connect()
                await ctx.send(f"Connected to {channel}")
        except AttributeError:  # Invoker is not in a voice channel.
            await ctx.send("You need to be in a voice channel for me to join..")


def setup(client: discord.ext.commands.bot.Bot) -> None:
    """
    Loads the Music cog.
    """
    client.add_cog(Music(client))

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from random import choice
import asyncio


class Miscellaneous(commands.Cog):
    """
    A cog class containing commands that have no particular grouping; miscellaneous
    commands.
    """
    client: Bot

    def __init__(self, client: Bot) -> None:
        """
        Initialize the Miscellaneous cog.
        """
        self.client = client

    @commands.command(name='coinflip', aliases=['flip', 'coin_flip', 'head_tails'])
    async def coinflip(self, ctx: Context) -> None:
        """
        Flips a coin.
        """
        coin = ['heads', 'tails']
        result = choice(coin)
        async with ctx.typing():
            msg: discord.message.Message = await ctx.send("🪙 **Flipping a coin**")
            for i in range(3):  # Message loading aesthetic
                await asyncio.sleep(0.25)
                await msg.edit(content=f"{msg.content}.")
        await msg.edit(content=f"{msg.content}***{result.upper()}***")

    @commands.command(name='choose', aliases=['choice'])
    async def choose(self, ctx: Context, *, options: str = None) -> None:
        """
        Chooses from a list of items separated by commas.
        """
        try:
            chosen = choice(options.split(',')).rstrip().lstrip()
        except (IndexError, AttributeError):  # when options is empty or None
            await ctx.send("You've given me no choices.")
            return None

        await ctx.send(f"🤔 I choose **{chosen}**")

    @commands.command(name='say', aliases=['repeat'])
    async def repeat(self, ctx: Context, *, msg: str = None) -> None:
        """
        The bot will repeat the message <msg> sent by the invoker and deletes the invokers
        command call.
        :param ctx: Context
        :param msg: The phrase the invoker wants repeated by the bot
        """
        if not msg:  # No message was given; msg is None or msg = ''
            return None
        await ctx.send(msg)
        await ctx.message.delete()


def setup(client: Bot) -> None:
    """
    Loads the Miscellaneous cog.
    """
    client.add_cog(Miscellaneous(client))

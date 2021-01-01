import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from youtube_search import YoutubeSearch


class Search(commands.Cog):
    """
    A class containing commands used for searching the web.
    """
    client: Bot

    def __init__(self, client: Bot) -> None:
        """
        Initializes this cog.
        """
        self.client = client

    @commands.command(name='youtube', aliases=['yt', 'YT', "Youtube", "YouTube"])
    async def youtube_search(self, ctx: Context, *, query: str = None) -> None:
        """
        Outputs a youtube link related to the search term <query>
        """
        if not query:  # No query was given.
            return None

        results = YoutubeSearch(query, max_results=1).to_dict()

        if not results:
            await ctx.send("No result found 😔")
            return None
        url = f"https://www.youtube.com{results[0].get('url_suffix')}"
        await ctx.send(f"🖥️ | {url}")


def setup(client: Bot) -> None:
    """
    Loads the Search cog.
    """
    client.add_cog(Search(client))

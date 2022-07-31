from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from youtube_search import YoutubeSearch
import requests, random, discord, wikipedia


colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0x00FFFF, 0xFF00FF, 0xff00ff, 0x99ccff, 0x66ff99]


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

    @commands.command(name='youtube', aliases=['yt'])
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

    @commands.command(name = "urban_dictionary", aliases = ["urban", "ud"])
    async def urban(self, ctx, *, query):
        fixed_query = query.replace(" ", "+")
        link = f"http://api.urbandictionary.com/v0/define?term={fixed_query}"
        resp = requests.get(link)
        info = dict(resp.json())
        
        options = info.get("list")[:3]
        if len(options) == 0:       
            await ctx.send("No results Found 😔")
            return
        
        choice = random.choice(options)
        definition = discord.Embed(
            title=f"{choice['word']} by {choice['author']}",
            description=f"{choice['definition']}",
            url=choice['permalink'],
            color=0x1d7ae2
        )
        definition.add_field(name="Example(s)", value = f"{choice['example']}", inline = False)
        definition.add_field(name="Votes", value=f"👍 {choice['thumbs_up']} | 👎 {choice['thumbs_down']}")
        definition.set_thumbnail(url="https://cdn.discordapp.com/attachments/709158571278860298/727611798039036044/urban_dictionary.png")
        await ctx.send(embed=definition)
        
    @commands.command(name = "wiki", aliases = ["wp", "wikipedia"])
    async def wiki(self, ctx, *, query=None):
        if query is not None:
            # Make a search for relevant results then ask the searcher which one he wants
            results = wikipedia.search(query)
            res_str = ""
            for i in range(len(results)):
                if i + 1 != len(results):
                    res_str += f"{i + 1}) {results[i]}\n"
                else:
                    res_str += f"{i + 1}) {results[i]}"

            color_choice = random.choice(colors)
            results_embed = discord.Embed(
                title = f"Select one of the following by inputting their corresponding number (1-{len(results)}).",
                description = res_str,
                color = color_choice
            )
            
            await ctx.send(embed=results_embed)
            channel = ctx.channel
            author = ctx.author.id
            def check(m):
                try:
                    return 1 <= int(m.content) <= 4 and m.channel == channel and ctx.author.id == author
                except ValueError:
                    pass
            msg = await self.client.wait_for("message", check=check)
            choice = results[int(msg.content) - 1]
            page = wikipedia.page(choice)
            
            page_title = page.title
            page_summary = page.summary
            page_url = page.url
            page_image = ""
            for image in page.images:
                if "png" in image or "jpg" in image or "jpeg" in image:
                    page_image = image
                    break
            final_embed = discord.Embed(
                title = page_title,
                url = page_url,
                color = color_choice
            )
            final_embed.set_thumbnail(url = page_image)
            final_embed.add_field(name = "Summary", value = f"{page_summary[:1000]}...")
            await ctx.send(embed=final_embed)

def setup(client: Bot) -> None:
    """
    Loads the Search cog.
    """
    client.add_cog(Search(client))

import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands.bot import Bot
from embed_maker import profile_embed


class Social(commands.Cog):
    """
    A cog class that deals with the social aspect of discord.
    """
    client: Bot
    embed_color: int

    def __init__(self, client: Bot) -> None:
        """
        Initializes this cog.
        """
        self.client = client
        self.embed_color = 0x1e38fa

    @commands.command(name='profile')
    async def profile(self, ctx: Context) -> None:
        """
        If there are no mentions, outputs information about the account of the invoker
        otherwise outputs the avatar of the person(s) that was mentioned.
        """
        msg: discord.message.Message = ctx.message

        if msg.mentions:
            for member in msg.mentions:
                embed = profile_embed(ctx.author, member, self.embed_color)

                await ctx.send(embed=embed)
        else:
            embed = profile_embed(ctx.author, ctx.author, self.embed_color)
            await ctx.send(embed=embed)

    @commands.command(name='avatar')
    async def avatar(self, ctx: Context) -> None:
        """
        If there are no mentions, outputs the avatar of the invoker otherwise outputs
        the avatar of the person(s) that was mentioned.
        """
        msg: discord.message.Message = ctx.message

        if not msg.mentions:  # There are no mentions | invoker wants their pfp.
            invoker: discord.member.Member = ctx.author
            avatar_embed = discord.Embed(
                title=f'{invoker.name}#{invoker.discriminator}',
                description=f"**[Avatar URL]({invoker.avatar_url})**",
                color=self.embed_color
            )
            avatar_embed.set_image(url=invoker.avatar_url)
            await ctx.send(embed=avatar_embed)
        else:  # There are mentions | Invoker wants other peoples' pfp.
            for member in msg.mentions:  # Make a new embed for every mention
                avatar_embed = discord.Embed(
                    title=f'{member.name}#{member.discriminator}',
                    description=f"**[Avatar URL]({member.avatar_url})**",
                    color=self.embed_color
                )
                avatar_embed.set_image(url=member.avatar_url)
                await ctx.send(embed=avatar_embed)


def setup(client: Bot) -> None:
    client.add_cog(Social(client))

"""
Commands:
    - Purge <n>: Deletes the last n number of messages sent in the channel it was called in.
"""

import os, discord, random, asyncio, sys
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.is_owner()
    @commands.has_permissions(manage_messages=True, manage_roles=True)
    @commands.command(name = 'purge')
    async def purge(self, ctx, *, amount=1):
        try:
            amount = int(amount) + 1
        except ValueError:
            return
        await ctx.channel.purge(limit=amount)
    
def setup(client):
    client.add_cog(Moderation(client))
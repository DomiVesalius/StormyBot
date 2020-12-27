"""
This is the main module for Stormy.
Run this file for Stormy to start up.
"""

import discord, asyncio, os, random
from discord.ext import commands
from dotenv import load_dotenv

CLIENT = commands.Bot(command_prefix='>')  # Bot instance


async def change_status() -> None:
    """
    A function that handles changing the status of the client.
    """
    await CLIENT.wait_until_ready()
    status_messages = ["Ring of Elysium", "Overwatch", "Valorant",
                       "Grand Theft Auto V", "MapleStory 2",
                       "Taking your derivative ( ͡° ͜ʖ ͡°)",
                       "Bopping chanchan with kendo sticc",
                       'Flaming Shady 🔥', 'Studying']
    print('All Systems Operational')

    while not CLIENT.is_closed():
        status = random.choice(status_messages)
        await CLIENT.change_presence(activity=discord.Game(status))
        await asyncio.sleep(1500)


@CLIENT.command()
@commands.is_owner()
async def reload(ctx):  # Reloads all the cogs
    """
    Reloads all cogs
    Restricted to owner.
    """
    for file_name in os.listdir('./cogs'):
        if file_name.endswith('.py'):
            CLIENT.unload_extension(f"cogs.{file_name[:-3]}")
            CLIENT.load_extension(f"cogs.{file_name[:-3]}")
            print(f"Reloaded {file_name}")
    await ctx.send("All commands reloaded!")


if __name__ == "__main__":
    # Look in the directory in the cogs folder give all files within it.
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):  # Checking if it is a python file.
            CLIENT.load_extension(f'cogs.{filename[:-3]}')
            print(f"{filename}")

    load_dotenv(dotenv_path='.env')
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CLIENT.remove_command('help')
    CLIENT.loop.create_task(change_status())
    CLIENT.run(BOT_TOKEN)

from discord import Embed
from lib.audio import Audio
from discord.member import Member


def enqueue_embed(audio: Audio, requester: str) -> Embed:
    """
    Returns a discord embed containing information about the audio that has been added to
    the queue.
    :param requester: The person that triggered the command.
    :param audio: The Audio object containing information about the audio that is queued.
    """
    embed = Embed()
    embed.add_field(name="ENQUEUED! 🎵",
                    value=f"Queued [{audio.get_title()}]({audio.get_video_url()}) "
                          f"[{requester}]")
    embed.add_field(name="⠀", value=f"``[{audio.get_duration()}]``")
    return embed


def now_playing_embed(audio: Audio, requester: str) -> Embed:
    """
    Returns a discord embed containing information about the audio that is now playing.
    :param audio: The Audio object containing information about the audio that is playing.
    :param requester: The user that requested this song.
    """
    embed = Embed()
    embed.add_field(name="Now Playing! 🎵",
                    value=f"[{audio.get_title()}]({audio.get_video_url()})\n"
                          f"``[{audio.get_duration()}]``")
    embed.add_field(name="⠀", value=f"Requested by: {requester}", inline=False)
    embed.set_thumbnail(url=audio.get_thumbnail())
    return embed


def profile_embed(author: Member, member: Member, embed_color: int) -> Embed:
    """
    Returns a discord embed containing information about the <member>'s profile.
    """
    embed = Embed(color=embed_color)
    embed.set_author(name=f"{member.name}#{member.discriminator}'s Profile",
                     icon_url=member.avatar_url)
    embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar_url)

    roles = ""
    day, month = member.joined_at.day, member.joined_at.month
    year = member.joined_at.year
    embed.add_field(name='Joined at:', value=f"{year}-{month}-{day}")

    for role in member.roles:
        if role.is_default():  # if the role is @everyone
            roles += f"{role} "
        else:
            roles += f"{role.mention} "
    embed.add_field(name=f'Roles ({len(member.roles)}):', value=roles, inline=False)
    embed.add_field(name=f'Top Role:', value=member.top_role.mention, inline=False)

    return embed

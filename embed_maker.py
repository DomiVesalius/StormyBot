from discord import Embed
from lib.audio import Audio


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

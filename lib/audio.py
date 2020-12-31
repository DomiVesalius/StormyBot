from typing import List


class Audio:
    """
    A class representing the audio of a YouTube video.

    ==Attributes==
    - id: The id for this audio.
    - title: The title of the audio
    - thumbnails: The thumbnail of this audio.
    - duration: The duration of this audio.
    - url: The youtube url of this audio.
    - channel: The youtube channel that this audio was posted to.
    """
    id: str
    title: str
    thumbnails: List[str]
    duration: str
    audio_url: str
    video_url: str
    channel: str

    def __init__(self, dict_: dict) -> None:
        """
        Initializes this audio object.
        :param dict_: A dictionary containing data about the audio
        """
        self.id = dict_.get('id')
        self.title = dict_.get('title')
        self.thumbnails = dict_.get('thumbnails')
        self.duration = dict_.get('duration')
        self.audio_url = dict_.get('audio_link')
        self.video_url = dict_.get('video_link')
        self.channel = dict_.get('channel')

    def __str__(self) -> str:
        """
        Returns a string representation of this audio.
        """
        res = f"{self.title} [{self.duration}]"
        return res

    def get_id(self) -> str:
        """
        Returns the id of this audio.
        """
        return self.id

    def get_title(self) -> str:
        """
        Returns the title of this audio.
        """
        return self.title

    def get_thumbnail(self) -> str:
        """
        Returns a thumbnail for this audio.
        """
        if not self.thumbnails:
            return ''

        return self.thumbnails[0]

    def get_duration(self) -> str:
        """
        Returns the duration of this audio.
        """
        return self.duration

    def get_video_url(self) -> str:
        """
        Returns the url of this audios video.
        """
        return self.video_url

    def get_audio_url(self) -> str:
        """
        Returns the url of this audios.
        """
        return self.audio_url

    def get_channel(self) -> str:
        """
        Returns the channel that uploaded the video that this audio comes from.
        """
        return self.channel

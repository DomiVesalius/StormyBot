# StormyBot

### **Feature Logs**:
**Voice Functionality** - December 31, 2020
* ``join``:
    * Makes Stormy join the voice channel you are in, if Stormy isn't already in a 
      channel.
* ``leave``:
    * Makes Stormy leave the voice channel she is in.
* ``play <query/>``:
    * Stormy will play the first search result given the query term.
    * This command can take in both search terms and youtube links.
    * Will act as a pause/resume command if no query is specified.
* ``loop``:
    * Changes the status of the queue to loop audio in the queue.
    * Every time a new audio is played, it is added back into the end of the queue.
* ``pause:``
    * If there is a song that is currently playing, pauses audio playback.
    * If there is not song that is currently playing (ie playback is paused), then audio
      playback is resumed.
* ``skip``:
    * Skips the song that is currently playing.
*  ``queue``:
    * Outputs the songs that are still in the queue.

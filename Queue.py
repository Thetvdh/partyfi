import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv(".env")


class Queue:

    def __init__(self):
        scope = "user-read-playback-state user-read-currently-playing user-modify-playback-state"
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def api_get_queue(self):
        return self.spotify.queue()

    def parse_queue(self, queue):
        parsed_queue = []
        if queue['currently_playing'] is not None:
            print("[QUEUE]: ", queue)
            song_name = queue['currently_playing']['name']
            song_artist = queue['currently_playing']['artists'][0]['name']

            song = {
                "title": song_name,
                "artist": song_artist
            }
        else:
            song = {
                "title": "Nothing Currently playing",
                "artist": "No Artist"
            }
        parsed_queue.append(song)
        for track in queue['queue']:
            song_name = track['name']
            song_artist = track['artists'][0]['name']

            song = {
                "title": song_name,
                "artist": song_artist
            }
            parsed_queue.append(song)
        return parsed_queue

    def get_queue(self):
        queue = self.api_get_queue()
        return self.parse_queue(queue)

    def add_to_queue(self, uri):
        try:
            self.spotify.add_to_queue(uri)
            return True
        except spotipy.exceptions.SpotifyException:
            return False

    def skip(self):
        self.spotify.next_track()


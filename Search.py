import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint


class Search:

    def __init__(self):
        self.spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    def api_get_tracks(self, name):
        name_list = name.split("||")
        print("NAME LIST", name_list)
        if len(name_list) > 1:
            query = "track:" + name_list[0] + "artist:" + name_list[1]
            print("QUERY:", query)
            results = self.spotify.search(q=query, type='track')
            pprint(results)
        else:
            results = self.spotify.search(q='track:' + name, type='track')
        tracks = results['tracks']['items']
        return tracks

    def parse_tracks(self, tracks, debug=False):

        new_data = []
        for track in tracks:
            song_name = track['name']
            song_uri = track['uri']
            song_artist = track['artists'][0]['name']

            song = {
                "title": song_name,
                "artist": song_artist,
                "uri": song_uri
            }

            new_data.append(song)

        return new_data

    def get_tracks(self, title, debug=False):
        tracks = self.api_get_tracks(title)
        return self.parse_tracks(tracks, debug)

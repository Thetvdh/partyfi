import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv(".env")
if os.path.isfile(".cache"):
    os.remove(".cache")

scope = "user-read-playback-state user-read-currently-playing user-modify-playback-state"
auth_manager = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
print(auth_manager.queue())

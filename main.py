import spotipy, os, pprint as pr
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv

from src.data_processing import *
from src.spotify_data import *
from src.telegram_bot import *
from src.spotify_utils import *
from utils import *


load_dotenv()

"""
SpotiPy instance to fetch authenticate connection to Spotify API
"""
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

spotify_scopes = "playlist-read-private playlist-modify-private playlist-modify-public user-read-recently-played user-top-read user-library-modify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8000/callback",
                                               scope=spotify_scopes))

audio_features = []
current_dir = os.path.dirname(os.path.abspath(__file__))

def pprint(text):
    pr.pprint(text, sort_dicts=False)

"""
Module initializer
"""

def main():
    results = get_spotify_search(sp, genre='afterglow')
    
    track_artist_genres = []
    for track in results['tracks']:
        track_uri = track['track_uri']
        print(f"{track['track_name']}:{track['track_href']}")
        track_artist_genres.append(get_artist_genre(sp, track_uri))
    print(track_artist_genres)


if __name__ == "__main__":
    main()
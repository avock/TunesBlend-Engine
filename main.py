import spotipy, os, pprint as pr
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv

from src.data_processing import *
from src.spotify_data import *
from src.telegram_bot import *
from src.spotify_utils import *
from src.constants import *
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
                                               redirect_uri="http://127.0.0.1:8000/callback",
                                               scope=spotify_scopes))

audio_features = []
current_dir = os.path.dirname(os.path.abspath(__file__))

def pprint(text):
    pr.pprint(text, sort_dicts=False)



"""
Module initializer
"""

def main():
    # for genre in global_genres[:1]:
    #     pprint(get_spotify_search(sp, 50, genre=genre))
    #     print(genre)
    track_uri = 'spotify:track:4h8VwCb1MTGoLKueQ1WgbD'
    search_track_name = 'The Nights'
    
    # print(get_audio_features(sp, (get_spotify_search(sp, track=search_track_name))['tracks'][0]['track_uri']))
    print(get_audio_features(sp, track_uri))
    # pprint(get_track_details(sp, track_uri))

        
if __name__ == "__main__":
    main()
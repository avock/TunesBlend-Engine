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
    # genre_list = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']
    
    # # results = get_spotify_search(sp, genre='british blues')
    # results = (get_spotify_recommendation(sp, seed_genres=['acoustic']))
    
    # track_artist_genres = []
    # for track in results:
    #     track_uri = track['track_uri']
    #     print(f"{track['track_name']}:{track['track_href']}")
    #     track_artist_genres.append(get_artist_genre(sp, track_uri))
    # print(get_all_genres(track_artist_genres))
    print((extract_genres('https://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity')))



if __name__ == "__main__":
    main()
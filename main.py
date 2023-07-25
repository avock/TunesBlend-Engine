import spotipy, os, pprint
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

from src.data_processing import *
from src.spotify_data import *

load_dotenv()

"""
SpotiPy instance to fetch authenticate connection to Spotify API
"""
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

audio_features = []
current_dir = os.path.dirname(os.path.abspath(__file__))

# loops through all 10 raw_data_files
for i in range(10):

    relative_raw_data_path = f'data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
    raw_data_path = os.path.join(current_dir, relative_raw_data_path)
    
    relative_processed_data_path = f'data/processed_data/clean-data_{i*1000}-{(i+1)*1000 - 1}.csv'
    processed_data_path = os.path.join(current_dir, relative_processed_data_path)
    
    json_data = read_data(raw_data_path)

    for playlist in json_data['playlists'][:3]:

        audio_features_list = get_playlist_audio_features(playlist, sp)

        audio_features.extend(audio_features_list)

    write_data(audio_features, processed_data_path)

    # Reset audio_features_list for the next raw_data_file
    audio_features = []
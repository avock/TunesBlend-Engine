import spotipy, os, pprint, subprocess, matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv


from src.data_processing import *
from src.spotify_data import *
from src.telegram_bot import *
from src.spotify_utils import *


load_dotenv()

"""
DO NOT REMOVE SpotiPy instance to fetch authenticate connection to Spotify API
"""
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

spotify_scopes = "playlist-read-private playlist-modify-private playlist-modify-public user-read-recently-played user-top-read user-library-modify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8000/callback",
                                               scope=spotify_scopes))

current_dir = os.path.dirname(os.path.abspath(__file__))

"""
Function to test spotify API
"""
def spotify_api_test():
    audio_feature = get_audio_features(sp, 'spotify:track:0UaMYEvWZi0ZqiDOoHU3YI')
    print(audio_feature)



"""
Function to fetch Audio Features from playlist json
"""
def get_playlist_details_from_file():

    playlist_details = []
    
    # loops through all 10 raw_data_files
    for i in range(3, 10):
        if i == 6 or i == 7:
            print(f'Skipping file {i*1000}-{(i+1)*1000 - 1}')
            continue

        relative_raw_data_path = f'data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
        raw_data_path = os.path.join(current_dir, relative_raw_data_path)
        
        relative_processed_data_path = f'data/processed_data/playlist_details/details-{i*1000}-{(i+1)*1000 - 1}.csv'
        processed_data_path = os.path.join(current_dir, relative_processed_data_path)
        
        json_data = read_data(raw_data_path)
        for playlist in json_data['playlists']:
            playlist_details_list = get_playlist_details(playlist, sp)

            playlist_details.extend(playlist_details_list)

        write_data(playlist_details, processed_data_path)

        # Reset playlist_details_list for the next raw_data_file
        playlist_details = []



"""
Function to fetch Audio Features from playlist json
"""
def get_audio_features_from_file():
    
    audio_features = []

    # loops through all 10 raw_data_files
    for i in range(1, 10):

        relative_raw_data_path = f'data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
        raw_data_path = os.path.join(current_dir, relative_raw_data_path)
        
        relative_processed_data_path = f'data/processed_data/audio_features/audio_features-{i*1000}-{(i+1)*1000 - 1}.csv'
        processed_data_path = os.path.join(current_dir, relative_processed_data_path)
        
        json_data = read_data(raw_data_path)
        for playlist in json_data['playlists']:
            audio_features_list = get_playlist_audio_features(playlist, sp)

            audio_features.extend(audio_features_list)

        write_data(audio_features, processed_data_path)

        # Reset audio_features_list for the next raw_data_file
        audio_features = []



"""
Function to fetch Audio Features from playlist json
"""
def get_genres_from_file():

    genres = []

    # loops through all 10 raw_data_files
    for i in range(1, 10)[:1]:

        relative_raw_data_path = f'data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
        raw_data_path = os.path.join(current_dir, relative_raw_data_path)
        
        relative_processed_data_path = f'data/processed_data/genres/genres-{i*1000}-{(i+1)*1000 - 1}.csv'
        processed_data_path = os.path.join(current_dir, relative_processed_data_path)
        
        json_data = read_data(raw_data_path)
        for playlist in json_data['playlists'][:1]:
            audio_features_list = get_playlist_genres(playlist, sp)

            genres.extend(audio_features_list)

        write_data(genres, processed_data_path)

        # Reset audio_features_list for the next raw_data_file
        genres = []

"""
Function to get genre of track(s)
"""
track_id = '5Iy2Jj87Ha0C0IBlNE1I4y'
track2_id = '0ct6r3EGTcMLPtrXHDvVjc'
track3_id = 'spotify:track:0UaMYEvWZi0ZqiDOoHU3YI'


# Individual Tracks
def get_playlist_track_genre_individual():
    track_details = sp.track(track3_id)

    artist_id = track_details['artists'][0]['id']
    album_id = track_details['album']['id']

    artist_genre = sp.artist(artist_id)['genres']
    album_genre = sp.album(album_id)['genres']

    print(f"Artist Genre: {artist_genre}")
    print(f"Album Genre: {album_genre}")

# Multiple Tracks
def get_playlist_track_genre_multiple():
    tracks = [track_id, track2_id, track3_id]

    artist_id_list = [track['artists'][0]['id'] for track in track_details_list['tracks']]
    album_id_list = [track['album']['id'] for track in track_details_list['tracks']]

    artist_genre_list = [sp.artist(artist)['genres'] for artist in artist_id_list]
    album_genre_list = [sp.album(album)['genres'] for album in album_id_list]

    print(f"Artist Genre: {artist_genre_list}")
    print(f"Album Genre: {album_genre_list}")


"""
Function to obtain mean, 25 and 75-percentile of each playlist audio_feature
"""
def get_audio_feature_data():
    source_file = f'data/processed_data/clean-data.csv'
    source_path = os.path.join(current_dir, source_file)

    target_file = f'data/processed_data/clean-data-agg.csv'
    target_path = os.path.join(current_dir, target_file)

    get_playlist_data(source_path, target_path)

    
    
"""
Extracts all genres from everynoise.com
"""
import requests
from bs4 import BeautifulSoup

def extract_genres():
    response = requests.get('https://everynoise.com/everynoise1d.cgi?scope=all&vector=popularity')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        genres = []

        # Find all table rows ('tr') in the webpage
        rows = soup.find_all('tr')

        for row in rows:
            # Find the genre in the third column ('td') of the row
            genre = row.find_all('td')[2].text.strip()
            if genre:
                genres.append(genre)

        return genres

    else:
        print("Failed to fetch the webpage.")
        return []
    
def get_user_playlists_utils() -> list:
    user_playlists = get_user_playlists(sp)
    return user_playlists

def test():
    return 'test'
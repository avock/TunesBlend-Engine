import spotipy, os, pprint, subprocess, matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from dotenv import load_dotenv


from src.data_processing import *
from src.spotify_data import *
from src.telegram_bot import *
from src.spotify_utils import *
from src.constants import *


load_dotenv()

"""
DO NOT REMOVE SpotiPy instance to fetch authenticate connection to Spotify API
"""
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

spotify_scopes = "playlist-read-private playlist-modify-private playlist-modify-public user-read-recently-played user-top-read user-library-modify"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://127.0.0.1:8000/callback",
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
    for i in range(0, 10):

        relative_raw_data_path = f'data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
        raw_data_path = os.path.join(current_dir, relative_raw_data_path)
        
        relative_processed_data_path = f'data/processed_data/genres/test1-genres-{i*1000}-{(i+1)*1000 - 1}.csv'
        processed_data_path = os.path.join(current_dir, relative_processed_data_path)
        
        json_data = read_data(raw_data_path)
        for playlist in json_data['playlists']:
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
    
    
    
"""
Extracts updated genre list from everynoise.com and compares to current list
"""
def get_missing_genres():
    new_genre_list = extract_genres()
    missing_genres = [genre for genre in new_genre_list if genre not in global_genres]
    
    if not missing_genres:
        return 'No New Genres Found.'
    
    return missing_genres    

def get_audio_features_by_genre():
    relative_processed_data_path = f'data/processed_data/genres/audio_features_by_genre.csv'
    processed_data_path = os.path.join(current_dir, relative_processed_data_path)
    
    total_genres = len(global_genres)
    
    for idx, genre in enumerate(global_genres):
        
        try:
            if idx % 100 == 0:
                status_update_message = f'Analyzing Genre {idx}: {genre.capitalize()}. {round(idx*100/total_genres, 2)}% completed.'
                print(status_update_message)
                send_message(status_update_message, chat_id_dev)
            
            genre_tracks = get_spotify_search(sp, 50, genre=genre)['tracks']
            
            track_uri_list = []
            combined_list = []
            
            # reformatting track JSON object to remove unecessary information
            
            unique_tracks = []
            for idx, track in enumerate(genre_tracks):
                if track['track_uri'] not in unique_tracks:
                    new_track = {
                        'genre': genre,
                        'track_name': track['track_name'],
                        'track_uri': track['track_uri']
                    }
                    genre_tracks[idx] = new_track
            
            # extrac†ing list of track_uris to retrieve audio_features
            for track in genre_tracks:
                track_uri = track['track_uri']
                track_uri_list.append(track_uri)

            audio_features_list = get_audio_features(sp, track_uri_list)
            
            for idx, track in enumerate(genre_tracks):
                if idx < len(audio_features_list):
                    track.update(audio_features_list[idx])
                    combined_list.append(track)
            
            write_data(combined_list, processed_data_path)
        
        except Exception as e:
            error_message = f'An error occured at genre_idx = {idx}. Error: {e}'
            print(error_message)
            send_message(error_message)
        
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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri="http://localhost:8000/callback",
                                               scope="user-library-read"))

current_dir = os.path.dirname(os.path.abspath(__file__))

"""
Function to test spotify API
"""
def spotify_api_test():
    audio_feature = get_audio_features('spotify:track:0UaMYEvWZi0ZqiDOoHU3YI', sp)
    print(audio_feature)



"""
Function to fetch Audio Features from playlist json
"""
def get_all_audio_features():
    # loops through all 10 raw_data_files
    for i in range(9, 10):

        relative_raw_data_path = f'data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
        raw_data_path = os.path.join(current_dir, relative_raw_data_path)
        
        relative_processed_data_path = f'data/processed_data/audio_features/audio_features_{i*1000}-{(i+1)*1000 - 1}.csv'
        processed_data_path = os.path.join(current_dir, relative_processed_data_path)
        
        json_data = read_data(raw_data_path)
        for playlist in json_data['playlists']:
            audio_features_list = get_playlist_audio_features(playlist, sp)

            audio_features.extend(audio_features_list)

        write_data(audio_features, processed_data_path)

        # Reset audio_features_list for the next raw_data_file
        audio_features = []

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
Function to get genre of each playlist and the overall genre
"""
def get_overall_genre():
    audio_features = []
    genre_list = []
    
    for i in range(10):
        relative_raw_data_path = f'data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
        raw_data_path = os.path.join(current_dir, relative_raw_data_path)
        
        relative_processed_data_path = f'data/processed_data/genre/genre_{i*1000}-{(i+1)*1000 - 1}.csv'
        processed_data_path = os.path.join(current_dir, relative_processed_data_path)
        
        try:
            json_data = read_data(raw_data_path)
            for playlist in json_data['playlists']:
                audio_features_list = get_playlist_track_genre(playlist, sp)
                audio_features.extend(audio_features_list)

            genre_list.extend(audio_features)

            print(f"Genre for file {i}: {genre_list}")
            send_message(f"Genre for file {i}: {genre_list}")
            
            # Reset audio_features_list for the next raw_data_file
            audio_features = []
            
        except Exception as e:
            print(f"Error processing file {i}: {str(e)}")

    print(f"Overall Genre List: {genre_list}")
    write_data(genre_list, processed_data_path)


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
Function to plot data and view trends of audio_features
"""
def get_audio_feature_graph():
    target_file = f'data/processed_data/clean-data-short.csv'
    target_path = os.path.join(current_dir, target_file)
    df = pd.read_csv(target_path)

    # Create the line plot with id values every 500
    plt.figure(figsize=(12, 6))  # Adjust the figure size as needed
    plt.plot(df['id'].iloc[::5000], df['key'].iloc[::5000], linestyle='-', linewidth=2)
    plt.xlabel('id')
    plt.ylabel('key')
    plt.title('Plot of key over id, showing every 500 ids')
    plt.grid(True)
    plt.tight_layout()  # Adjust the layout to prevent clipping of labels
    plt.show()
    
    
"""
"""

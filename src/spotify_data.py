import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pprint

load_dotenv()

"""
SpotiPy instance to fetch authenticate connection to Spotify API
"""
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

"""
List of features to be kept from the dataset
"""
target_audio_features = ['id', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

"""
Retrieves audio_features of a track

@param: Spotify Track URI
@return: Json object of target track's complete audio_features

"""
def get_audio_features(track_uri):
    audio_features = sp.audio_features(track_uri)[0]
    cleaned_audio_features = {target: audio_features[target] for target in target_audio_features if target in audio_features}
    return cleaned_audio_features

results = sp.artist_top_tracks('spotify:artist:36QJpDe2go2KgaRleHCDTp')
for track in results['tracks'][:10]:
    print('track    : ' + track['name'])
    print('audio    : ' + track['preview_url'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()
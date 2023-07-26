import datetime, pprint

from src.data_processing import *
from src.misc import *

"""
Function to retrieve audio_features of a track

@param: Spotify Track URI
@return: Json object of target track's complete + filtered audio_features

"""
def get_audio_features(track_uris, sp):
    audio_features = sp.audio_features(track_uris)
    filtered_audio_features = [filter_audio_feature(audio_feature) for audio_feature in audio_features]
    return filtered_audio_features



"""
Function to retrieve audio_features of every track in a playlist

@param: a playlist JSON object 
@return: Array of track_uri with globally unique identifier
"""
def get_playlist_audio_features(playlist, sp):
    
    audio_features_list = []
    track_uris = get_track_uris(playlist)
    playlist_id = playlist['pid']

    """
    Setup GVP VM to handle large amounts of data cleanup.
    Prints status every 100 playlist processed.
    """
    if playlist_id % 100 == 0:
        current_time = datetime.datetime.now()
        status_update_message = f'Begin processing playlist {playlist["pid"]} at {current_time}'
        print(status_update_message)
    
    """
    Setup Telegram Bot to send status update every 500 playlist processed.
    """        
    if playlist_id % 500 == 0 and playlist_id != 0:
        current_time = datetime.datetime.now()
        status_update_message = f'Begin processing playlist {playlist["pid"]} at {current_time}'
        send_telegram_message(status_update_message)

    chunk_size = 50
    track_id = 0
    
    for i in range(0, len(track_uris), chunk_size):
        chunk = track_uris[i:i + chunk_size]
        audio_features_chunk = get_audio_features(chunk, sp)

        pid = playlist['pid']
        for audio_feature in audio_features_chunk:
            id = f"{pid}_{track_id}"
            audio_feature['id'] = id
            audio_features_list.append(audio_feature)

    return audio_features_list



"""
Function to retreive the genre(s) of the album for one or multiple tracks.

@param track_uris: str or list - The track URI(s) for which to retrieve the genre(s).
@param sp: Spotipy object - The Spotipy client object for making API calls.

@return: list - The genre(s) of the album for the given track(s) in a list.
"""
def get_album_genre(track_uris, sp):

    if not isinstance(track_uris, list):
        
        track_details = sp.track(track_uris)
        album_id = track_details['album']['id']
        album_genre = sp.album(album_id)['genres']
        
        return album_genre
    else:

        track_details_list = sp.tracks(track_uris)
        album_id_list = [track['album']['id'] for track in track_details_list['tracks']]
        album_genre_list = [sp.album(album)['genres'] for album in album_id_list]

        return album_genre_list



"""
Function to retrieve the genre(s) of the artist for one or multiple tracks.

@param track_uris: str or list - The track URI(s) for which to retrieve the genre(s).
@param sp: Spotipy object - The Spotipy client object for making API calls.

@return: The genre(s) of the artist for the given track(s) in a list.
"""
def get_artist_genre(track_uris, sp):
    
    if not isinstance(track_uris, list):
        
        track_details = sp.track(track_uris)
        artist_id = track_details['artists'][0]['id']
        artist_genre = sp.artist(artist_id)['genres']
        
        return artist_genre
    
    else:

        track_details_list = sp.tracks(track_uris)
        artist_id_list = [track['artists'][0]['id'] for track in track_details_list['tracks']]
        artist_genre_list = [sp.artist(artist)['genres'] for artist in artist_id_list]

        return artist_genre_list



"""

"""
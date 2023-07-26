import datetime, pprint

from src.data_processing import *

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

    """
    Setup GVP VM to handle large amounts of data cleanup.s
    Prints status every 100 playlist processed.
    """
    if playlist['pid'] % 100 == 0:
        current_time = datetime.datetime.now()
        print(f'Begin processing playlist {playlist["pid"]} at {current_time}')

    chunk_size = 100
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
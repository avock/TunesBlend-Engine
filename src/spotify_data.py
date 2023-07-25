import datetime

from src.data_processing import *

"""
Function to retrieve audio_features of a track

@param: Spotify Track URI
@return: Json object of target track's complete + filtered audio_features

"""
def get_audio_features(track_uri, sp):
    audio_features = sp.audio_features(track_uri)[0]
    filtered_audio_features = filter_audio_feature(audio_features)
    return filtered_audio_features

"""
Function to retrieve audio_features of every track in a playlist

@param: a playlist JSON object 
@return: Array of track_uri with globally unique identifier
"""
def get_playlist_audio_features(playlist, sp):
    audio_features_list = []
    
    track_uris = get_track_uris(playlist)
    
    if (playlist['pid'] % 100 == 0):
        current_time = datetime.datetime.now()
        print(f'Started playlist {playlist["pid"]} at {current_time}')
    
    count = 0
    for track_uri in track_uris:
        audio_feature = get_audio_features(track_uri, sp)
        
        pid = playlist['pid']
        track_id = count; count+=1
        id = str(pid) + "_" + str(track_id)
        
        audio_feature['id'] = id
        
        audio_features_list.append(audio_feature)
    
    return audio_features_list
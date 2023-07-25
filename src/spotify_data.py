"""
List of features to be kept from the dataset
"""
target_audio_features = ['id', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']

"""
Function to retrieve audio_features of a track

@param: Spotify Track URI
@return: Json object of target track's complete audio_features

"""
def get_audio_features(track_uri, sp):
    audio_features = sp.audio_features(track_uri)[0]
    cleaned_audio_features = {target: audio_features[target] for target in target_audio_features if target in audio_features}
    return cleaned_audio_features

"""

"""
def get_playlist_audio_features(playlist, file_id, sp):
    
    audio_features_list = []
    
    track_uris = [track['track_uri'] for track in playlist['tracks']]
    pid = playlist['pid']
    file_id = file_id
    
    for track_uri in track_uris[:10]:
        audio_feature = get_audio_features(track_uri, sp)
        audio_feature['pid'] = pid
        audio_feature['file_id'] = file_id
        audio_features_list.append(audio_feature)
    
    return audio_features_list
import json, os, pandas as pd

"""
Function to read data from a JSON file

@param: pathname to a JSON file
@return: JSON object
"""
def read_data(json_file_path):
    with open(json_file_path, 'r') as file:
        json_data = json.load(file)
    return json_data

"""
Function to write data to a CSV file

@param: pathname to CSV file
@return: -
"""
def write_data(audio_features_list, file_path):
    audio_features_df = pd.DataFrame(audio_features_list)
    audio_features_df.to_csv(file_path, mode='a', index=False)

"""
Function to clean up audio_features of each track to target_features only

@param: Array of audio_features
@return: Array of target audio_features
"""
def filter_audio_feature(audio_features):

    # List of features to be kept from the dataset
    TARGET_AUDIO_FEATURES = ['id', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']
    
    target_audio_features = {target: audio_features[target] for target in TARGET_AUDIO_FEATURES if target in audio_features}
    return target_audio_features

"""
Function to extract uri of every track from playlist

@param: 
@return: array of track_uri with playlist_id appended to them
"""
def get_track_uris(playlist):
    track_uris =[track['track_uri'] for track in playlist['tracks']]
    return track_uris
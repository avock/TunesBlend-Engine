import json, os, pandas as pd
from itertools import zip_longest

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



"""
Remove duplicates from the input array and sort the elements in alphabetical order.

@param arr: A list or array containing elements.
@return: A new list with duplicates removed and elements sorted in alphabetical order.
"""
def arr_cleanup(arr):
    
    cleaned_arr = [sorted(list(set(sublist))) for sublist in arr]
    return cleaned_arr



"""
Combine two arrays of subarrays by pairing their elements together.

@param arr1, arr2: The first and second array of subarrays.

@return: A new array where each subarray contains elements paired from arr1 and arr2.
"""
def arr_combine(arr1, arr2):
    combined = []
    for sub_arr1, sub_arr2 in zip_longest(arr1, arr2):
        combined_sub_arr = []
        if sub_arr1:
            combined_sub_arr.extend(sub_arr1)
        if sub_arr2:
            combined_sub_arr.extend(sub_arr2)
        combined.append(combined_sub_arr)
    return combined



"""
Returns all unique genres present

@param: an array of array of genres 
@return: an array of every unique genre 
"""
def get_all_genres(array):
    all_genres = list(set(genre for genres in array for genre in genres))
    return sorted(all_genres)



"""
Converts nested array into nested json object
"""
def nested_array_to_json(audio_features, genre_list):
    result = []
    
    for subarray in audio_features:
        json_object = {genre: int(genre in subarray) for genre in genre_list}
        result.append(json_object)
    
    return result



"""
Obtains average of each audio feature based on playlist

@param: CSV containing audio feature of feach track within a playlist, and multiple playlists 
@return: CSV containing average audio feature of each playlist
"""
def get_playlist_average(source_csv_pathname, target_csv_pathname):
    data = pd.read_csv(source_csv_pathname)
    grouped_data = data.groupby(data['id'].str.split('_').str[0])
    
    audio_features_data = grouped_data.agg({
        'danceability': ['mean', 'min', 'max'],
        'energy': ['mean', 'min', 'max'],
        'key': ['mean', 'min', 'max'],
        'loudness': ['mean', 'min', 'max'],
        'speechiness': ['mean', 'min', 'max'],
        'acousticness': ['mean', 'min', 'max'],
        'instrumentalness': ['mean', 'min', 'max'],
        'liveness': ['mean', 'min', 'max'],
        'valence': ['mean', 'min', 'max'],
        'tempo': ['mean', 'min', 'max'],
        'duration_ms': ['mean', 'min', 'max']
    })
    
    audio_features_data.reset_index(inplace=True)
    
    new_data = pd.DataFrame({
        'id': audio_features_data.index,
        'danceability_min': audio_features_data[('danceability', 'min')],
        'danceability_max': audio_features_data[('danceability', 'max')],
        'danceability_mean': audio_features_data[('danceability', 'mean')],
        'energy_min': audio_features_data[('energy', 'min')],
        'energy_max': audio_features_data[('energy', 'max')],
        'energy_mean': audio_features_data[('energy', 'mean')],
        'key_min': audio_features_data[('key', 'min')],
        'key_max': audio_features_data[('key', 'max')],
        'key_mean': audio_features_data[('key', 'mean')],
        'loudness_min': audio_features_data[('loudness', 'min')],
        'loudness_max': audio_features_data[('loudness', 'max')],
        'loudness_mean': audio_features_data[('loudness', 'mean')],
        'speechiness_min': audio_features_data[('speechiness', 'min')],
        'speechiness_max': audio_features_data[('speechiness', 'max')],
        'speechiness_mean': audio_features_data[('speechiness', 'mean')],
        'acousticness_min': audio_features_data[('acousticness', 'min')],
        'acousticness_max': audio_features_data[('acousticness', 'max')],
        'acousticness_mean': audio_features_data[('acousticness', 'mean')],
        'instrumentalness_min': audio_features_data[('instrumentalness', 'min')],
        'instrumentalness_max': audio_features_data[('instrumentalness', 'max')],
        'instrumentalness_mean': audio_features_data[('instrumentalness', 'mean')],
        'liveness_min': audio_features_data[('liveness', 'min')],
        'liveness_max': audio_features_data[('liveness', 'max')],
        'liveness_mean': audio_features_data[('liveness', 'mean')],
        'valence_min': audio_features_data[('valence', 'min')],
        'valence_max': audio_features_data[('valence', 'max')],
        'valence_mean': audio_features_data[('valence', 'mean')],
        'tempo_min': audio_features_data[('tempo', 'min')],
        'tempo_max': audio_features_data[('tempo', 'max')],
        'tempo_mean': audio_features_data[('tempo', 'mean')],
        'duration_ms_min': audio_features_data[('duration_ms', 'min')],
        'duration_ms_max': audio_features_data[('duration_ms', 'max')],
        'duration_ms_mean': audio_features_data[('duration_ms', 'mean')]
    })

    new_data.to_csv(target_csv_pathname, index=False)

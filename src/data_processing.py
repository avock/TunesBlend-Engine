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
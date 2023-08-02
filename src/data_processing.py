import json, os, pandas as pd
from itertools import zip_longest
from collections import Counter

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

"""
def filter_track_details(track_details):
    if not isinstance (track_details, list):

        track_info = {
            'id': '',
            'track_uri': track_details['uri'],
            'track_title': track_details['name'],
            'track_url': track_details['external_urls']['spotify'],
            'track_popularity': track_details['popularity'],
            'release_date': track_details['album']['release_date'],
            'album_uri': track_details['album']['uri'],
        }
        return track_info
    else :

        track_details_list = []
        for track in track_details:
            if(track is None):
                print('None object obtained')
                continue

            track_info = {
                'id': '',
                'track_uri': track['uri'],
                'track_title': track['name'],
                'track_url': track['external_urls']['spotify'],
                'track_popularity': track['popularity'],
                'release_date': track['album']['release_date'],
                'album_uri': track['album']['uri'],
            }
            track_details_list.append(track_info)
        return track_details_list



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
@return: an array of (genre_name, genre_count) for every unique genre 
"""
def get_all_genres(array):
    # all_genres = list(set(genre for genres in array for genre in genres))
    # return sorted(all_genres)
    genre_counts = Counter(genre for genres in array for genre in genres)
    all_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)

    return all_genres


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
def get_playlist_data(source_csv_pathname, target_csv_pathname):
    data = pd.read_csv(source_csv_pathname)
    grouped_data = data.groupby(data['id'].str.split('_').str[0])
    
    audio_features_data = grouped_data.agg({
        'danceability': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'energy': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'key': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'loudness': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'speechiness': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'acousticness': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'instrumentalness': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'liveness': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'valence': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'tempo': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)],
        'duration_ms': ['mean', lambda x: x.quantile(0.25), lambda x: x.quantile(0.75)]
    })

    
    audio_features_data.reset_index(inplace=True)
    
    new_data = pd.DataFrame({
        'id': audio_features_data.index,
        'danceability_mean': audio_features_data[('danceability', 'mean')],
        'danceability_low': audio_features_data[('danceability', '<lambda_0>')],
        'danceability_high': audio_features_data[('danceability', '<lambda_1>')],
        'energy_mean': audio_features_data[('energy', 'mean')],
        'energy_low': audio_features_data[('energy', '<lambda_0>')],
        'energy_high': audio_features_data[('energy', '<lambda_1>')],
        'key_mean': audio_features_data[('key', 'mean')],
        'key_low': audio_features_data[('key', '<lambda_0>')],
        'key_high': audio_features_data[('key', '<lambda_1>')],
        'loudness_mean': audio_features_data[('loudness', 'mean')],
        'loudness_low': audio_features_data[('loudness', '<lambda_0>')],
        'loudness_high': audio_features_data[('loudness', '<lambda_1>')],
        'speechiness_mean': audio_features_data[('speechiness', 'mean')],
        'speechiness_low': audio_features_data[('speechiness', '<lambda_0>')],
        'speechiness_high': audio_features_data[('speechiness', '<lambda_1>')],
        'acousticness_mean': audio_features_data[('acousticness', 'mean')],
        'acousticness_low': audio_features_data[('acousticness', '<lambda_0>')],
        'acousticness_high': audio_features_data[('acousticness', '<lambda_1>')],
        'instrumentalness_mean': audio_features_data[('instrumentalness', 'mean')],
        'instrumentalness_low': audio_features_data[('instrumentalness', '<lambda_0>')],
        'instrumentalness_high': audio_features_data[('instrumentalness', '<lambda_1>')],
        'liveness_mean': audio_features_data[('liveness', 'mean')],
        'liveness_low': audio_features_data[('liveness', '<lambda_0>')],
        'liveness_high': audio_features_data[('liveness', '<lambda_1>')],
        'valence_mean': audio_features_data[('valence', 'mean')],
        'valence_low': audio_features_data[('valence', '<lambda_0>')],
        'valence_high': audio_features_data[('valence', '<lambda_1>')],
        'tempo_mean': audio_features_data[('tempo', 'mean')],
        'tempo_low': audio_features_data[('tempo', '<lambda_0>')],
        'tempo_high': audio_features_data[('tempo', '<lambda_1>')],
        'duration_ms_mean': audio_features_data[('duration_ms', 'mean')],
        'duration_ms_low': audio_features_data[('duration_ms', '<lambda_0>')],
        'duration_ms_high': audio_features_data[('duration_ms', '<lambda_1>')]
    })


    new_data.to_csv(target_csv_pathname, index=False)

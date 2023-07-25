import json, os, pandas as pd
from spotify_data import get_audio_features

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
Function to clean track data and get audio features
"""
def track_data_cleanup(playlist, file_id):
    pid = playlist['pid']
    file_id = file_id
    track_uris = [track['track_uri'] for track in playlist['tracks']]
    
    audio_features_list = []
    
    for track_uri in track_uris[:10]:
        audio_feature = get_audio_features(track_uri)
        audio_feature['pid'] = pid
        audio_feature['file_id'] = file_id
        audio_features_list.append(audio_feature)
    
    return audio_features_list

audio_features = []
current_dir = os.path.dirname(os.path.abspath(__file__))

# loops through all 10 raw_data_files
for i in range(10):

    relative_raw_data_path = f'../data/raw_data/mpd.slice.{i*1000}-{(i+1)*1000 - 1}.json'
    raw_data_path = os.path.join(current_dir, relative_raw_data_path)
    
    relative_processed_data_path = f'../data/processed_dataset/clean-data_{i*1000}-{(i+1)*1000 - 1}.csv'
    processed_data_path = os.path.join(current_dir, relative_processed_data_path)
    
    json_data = read_data(raw_data_path)

    for playlist in json_data['playlists'][:3]:

        audio_features_list = track_data_cleanup(playlist, i)

        audio_features.extend(audio_features_list)

    write_data(audio_features, processed_data_path)

    # Reset audio_features_list for the next raw_data_file
    audio_features = []

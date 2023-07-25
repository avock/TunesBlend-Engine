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

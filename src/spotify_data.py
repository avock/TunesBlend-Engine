import datetime, pprint, urllib.parse

from src.data_processing import *
from src.telegram_bot import *



def get_audio_features(sp, track_uris):
    audio_features = sp.audio_features(track_uris)
    filtered_audio_features = [filter_audio_feature(audio_feature) for audio_feature in audio_features]
    return filtered_audio_features



"""
Function to retreive the details of one or multiple tracks.
"""
def get_track_details(sp, track_uris):
    if not isinstance(track_uris, list):

        track_details = sp.track(track_uris)
        filtered_track_details = filter_track_details(track_details)
        
        return filtered_track_details
    else:

        track_details_list = sp.tracks(track_uris)['tracks']
        filtered_track_details_list = filter_track_details(track_details_list)

        return filtered_track_details_list



"""
Function to retreive the genre(s) of the album for one or multiple tracks.
"""
def get_album_genre(sp, track_uris):
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
"""
def get_artist_genre(sp, track_uris):
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
Returns an array of playlist dictionaries in the following format:
    ```
     {  
        'playlist_name': '//日本語  🇯🇵',
        'playlist_uri': 'spotify:playlist:0AfGrhDpHs17mj7pHeScPZ',
        'playlist_href': 'https://open.spotify.com/playlist/0AfGrhDpHs17mj7pHeScPZ',
        'playlist_track_count': 4
    }
    ```
"""
def get_user_playlists(sp):
    playlists = sp.current_user_playlists()['items']
    playlist_list = []
    for playlist in playlists:
        playlist_detail = {
            'playlist_name' : playlist['name'],
            'playlist_uri': playlist['uri'],
            'playlist_href': playlist['external_urls']['spotify'],
            'playlist_track_count': playlist['tracks']['total']
        }
        playlist_list.append(playlist_detail)
    
    return playlist_list



def get_user_playlist_count(sp):
    playlists = get_user_playlists(sp)
    return len(playlists)

"""
Returns the following:
    ```
    {
        'track_count' = TRACK_COUNT,
        'tracks' = [
            {
                'track_idx': 48,
                'track_name': 'Pompeii / Viva la Vida',
                'track_uri': 'spotify:track:1FOc6SLE7tFX0qeUx7WkPB',
                'track_href': 'https://open.spotify.com/track/1FOc6SLE7tFX0qeUx7WkPB',
                'artist': 'The Originals',
                'artist_uri': 'spotify:artist:2AQZTl6fUg5Ma83948E5S9',
                'album': 'Twenty Year Album',
                'album_uri': 'spotify:album:14zHan6dut5XvGFCmSNQIS'
            }, 
        ]
    }
    ```
"""
def get_playlist_tracks(sp, playlist_uri='spotify:playlist:6FS0wzsoprqRG9PAFsmVSz'):
    
    response = sp.playlist_tracks(playlist_uri, offset=0, limit=100)
    
    playlist_track_count = response['total']
    
    offset = 0
    tracks = []
    while offset < playlist_track_count:
        tracks_list = sp.playlist_tracks(playlist_uri, offset=offset, limit=100)['items']
        if not tracks_list:
            break
        tracks.extend(tracks_list)
        offset += 100
    
    track_list = []
    
    for idx, track in enumerate(tracks, start=1):
        track = track['track']
        track_info = {
            'track_idx': idx,
            'track_name': track['name'],
            'track_uri': track['uri'],
            'track_href': track['external_urls']['spotify'],
            'artist': track['artists'][0]['name'],
            'artist_uri': track['artists'][0]['uri'],
            'album': track['album']['name'],
            'album_uri': track['album']['uri'],
        }
        track_list.append(track_info)
    
    track_list = {
        'track_count': playlist_track_count,
        'tracks': track_list,
    }
    
    return track_list

"""
Note: Due to spotify's limitation, it is impossible to fetch > 100 top tracks for every user, the hard cap is 100
Returns the following dictionary:
    ```
    {
        'track_count' = TRACK_COUNT,
        'tracks' = [
            {
                'track_rank': 1,
                'track_name': 'Alone',
                'track_uri': 'spotify:track:3MEYFivt6bilQ9q9mFWZ4g',
                'track_href': 'https://open.spotify.com/track/3MEYFivt6bilQ9q9mFWZ4g',
                'artist': 'Marshmello',
                'artist_uri': 'spotify:artist:64KEffDW9EtZ1y2vBYgq8T',
                'album': 'Alone',
                'album_uri': 'spotify:album:7ePC9qS9mSOTY9E0YPP6yg'
            }, 
            ....
        ]
    }
    ```
"""
def get_user_top_tracks(sp, limit=10, time_range='long_term'):
    valid_time_ranges = ['short_term', 'medium_term', 'long_term']
    curr_offset = 0
    
    if time_range not in valid_time_ranges:
        raise ValueError('Value of range must be short_term (4 weeks), medium_term (6 months) or long_term (all time)')
    
    if limit > 100:
        raise ValueError('Value of limit must be less than 100')
    
    top_tracks = []
    track_list = []
    
    try:
        while curr_offset < limit - 1:
            curr_limit = 50 if limit-curr_offset > 50 else limit-curr_offset
            track_list.extend(sp.current_user_top_tracks(limit=curr_limit, offset=curr_offset, time_range=time_range)['items'])
            curr_offset += 49
        for idx, track in enumerate(track_list, start=1):
            track_info = {
                'track_rank': idx,
                'track_name': track['name'],
                'track_uri': track['uri'],
                'track_href': track['external_urls']['spotify'],
                'artist': track['artists'][0]['name'],
                'artist_uri': track['artists'][0]['uri'],
                'album': track['album']['name'],
                'album_uri': track['album']['uri'],
            }    
            top_tracks.append(track_info)
            
    except Exception as e:
        print(f"Error: {e}")
    
    return top_tracks



"""
Wrapper function to utilize spotify's search function. 
Possible filters: album, artist, track, year, upc, isrc, genre
"""
def get_spotify_search(sp, limit=10, type='track', **kwargs):
    search_filters = ['album', 'artist', 'track', 'year', 'upc', 'isrc', 'genre']
    search_boolean_filters = ['tag_hipster', 'tag_new']

    search_filters_param = {}

    for filter in search_filters:
        if filter in kwargs:
            search_filters_param[filter] = kwargs[filter].strip()

    for filter in search_boolean_filters:
        if filter in kwargs:
            search_filters_param[filter] = str(filter).replace('_', ':')

    query_string = ""
    
    for key, value in search_filters_param.items():
        if (key == 'tag_hipster' or key == 'tag_new'):
            query_string += (f"{value} ")
        else:
            query_string += (f'{key}:"{value}" ')
        
    query_string = str(query_string).strip()
    search_result = sp.search(q=query_string, limit=limit, type=type)
    
    search_result_list = []
    
    for idx, track in enumerate(search_result['tracks']['items'], start=1):
        track_info = {
            'track_idx': idx,
            'track_name': track['name'],
            'track_uri': track['uri'],
            'track_href': track['external_urls']['spotify'],
            'artist': track['artists'][0]['name'],
            'artist_uri': track['artists'][0]['uri'],
            'album': track['album']['name'],
            'album_uri': track['album']['uri'],
        }
        search_result_list.append(track_info)
    
    search_result = {
        'track_count': search_result['tracks']['total'],
        'tracks': search_result_list,
    }
    
    return search_result
    
    
    
"""
Retrieves Spotify recommendations based on various seed parameters and audio features

@param: (note: all are OPTIONAL) 
    - limit : number of tracks to return
    - seed_artists/genres/tracks
    - {various min/max/target)audio_features}
    
@return: An array of track dictionaries in the following format:
    ```
    {
        'track_rank': 1,
        'track_name': 'Could It Be',
        'track_uri': 'spotify:track:6fRKgExSY24i2whGdAJUnM',
        'track_href': 'https://open.spotify.com/track/6fRKgExSY24i2whGdAJUnM',
        'artist': 'Charlie Worsham',
        'artist_uri': 'spotify:artist:64KEffDW9EtZ1y2vBYgq8T',
        'album': 'Alone',
        'album_uri': 'spotify:album:7ePC9qS9mSOTY9E0YPP6yg' 
    }
    ```
"""
def get_spotify_recommendation(sp, limit=10, seed_artists=None, seed_genres=None, seed_tracks=None, country=None, **kwargs):
    cleaned_recommended_tracks = []
    
    audio_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'valence']
    audio_features_param = {}

    for feature in audio_features:
        feature_min = f'min_{feature}'
        feature_max = f'max_{feature}'
        feature_target = f'target_{feature}'
        
        for feature_param in [feature_min, feature_max, feature_target]:
            if feature_param in kwargs:
                audio_features_param[feature_param] = kwargs[feature_param]
            
    recommended_tracks = sp.recommendations(limit=limit, seed_artists=seed_artists, seed_genres=seed_genres, seed_tracks=seed_tracks, country=country, **audio_features_param)
    
    for idx, track in enumerate(recommended_tracks['tracks'], start=1):
        track_info = {
            'track_rank': idx,
            'track_name': track['name'],
            'track_uri': track['uri'],
            'track_href': track['external_urls']['spotify'],
            'artist': track['artists'][0]['name'],
            'artist_uri': 'spotify:artist:64KEffDW9EtZ1y2vBYgq8T',
            'album': 'Alone',
            'album_uri': 'spotify:album:7ePC9qS9mSOTY9E0YPP6yg'
        }
        cleaned_recommended_tracks.append(track_info)
        
    return cleaned_recommended_tracks
import datetime, pprint

from src.data_processing import *
from src.telegram_bot import *
from src.spotify_data import *



"""
Function to retrieve audio_features of every track in a playlist

@param: a playlist JSON object 
@return: Array of track_uri with globally unique identifier
"""
def get_playlist_audio_features(playlist, sp):
    
    audio_features_list = []
    track_uris = get_track_uris(playlist)
    playlist_id = playlist['pid']

    """
    Setup GVP VM to handle large amounts of data cleanup.
    Prints status every 100 playlist processed.
    """
    if playlist_id % 100 == 0:
        current_time = datetime.datetime.now()
        status_update_message = f'Begin processing playlist {playlist["pid"]} at {current_time}'
        print(status_update_message)
    
    """
    Setup Telegram Bot to send status update every 500 playlist processed.
    """        
    if playlist_id % 500 == 0 and playlist_id != 0:
        current_time = datetime.datetime.now()
        status_update_message = f'Begin processing playlist {playlist["pid"]} at {current_time}'
        send_message(status_update_message)

    chunk_size = 50
    track_id = 0
    
    for i in range(0, len(track_uris), chunk_size):
        chunk = track_uris[i:i + chunk_size]
        audio_features_chunk = get_audio_features(chunk, sp)

        pid = playlist['pid']
        for audio_feature in audio_features_chunk:
            id = f"{pid}_{track_id}"
            audio_feature['id'] = id
            audio_features_list.append(audio_feature)
            track_id += 1

    return audio_features_list



"""
"""
def get_playlist_details(playlist, sp):
    
    playlist_details_list = []
    track_uris = get_track_uris(playlist)
    playlist_id = playlist['pid']

    """
    Setup GVP VM to handle large amounts of data cleanup.
    Prints status every 100 playlist processed.
    """
    if playlist_id % 10 == 0:
        current_time = datetime.datetime.now()
        status_update_message = f'Begin processing playlist {playlist["pid"]} at {current_time}'
        print(status_update_message)
    
    """
    Setup Telegram Bot to send status update every 500 playlist processed.
    """        
    if playlist_id % 250 == 0 and playlist_id != 0:
        current_time = datetime.datetime.now()
        status_update_message = f'Begin processing playlist {playlist["pid"]} at {current_time}'
        send_message(status_update_message)

    chunk_size = 50
    track_id = 0
    
    for i in range(0, len(track_uris), chunk_size):
        chunk = track_uris[i:i + chunk_size]
        track_details_chunk = get_track_details(sp, chunk)
        
        pid = playlist['pid']
        
        for track_details in track_details_chunk:
            id = f"{pid}_{track_id}"
            track_details['id'] = id
            playlist_details_list.append(track_details)
            track_id += 1

    return playlist_details_list



"""
Combines get_album_genres() and get_artist_genre() to generate unified genre
* NOTE: as of 27/07/23, albums do NOT return any genres. So get_album_genres() removed for now, to save API calls

@param playlist to generate list of genre of each track

@return list of genre(s) of each track(s) in a list
"""
def get_playlist_track_genre(playlist, sp):
    genre_list = []
    track_uris = get_track_uris(playlist)
    playlist_id = playlist['pid']
    print(f'playlist {playlist["pid"]} at {datetime.datetime.now()}')

    """
    Setup GVP VM to handle large amounts of data cleanup.
    Prints status every 100 playlist processed.
    """
    if playlist_id % 100 == 0:
        current_time = datetime.datetime.now()
        status_update_message = f'WE`VE REACHED Playlist {playlist["pid"]} at {current_time}'
        print(status_update_message)
        send_message(status_update_message, chat_id_dev)
    
    """
    Setup Telegram Bot to send status update every 500 playlist processed.
    """        
    if playlist_id % 500 == 0 and playlist_id != 0:
        current_time = datetime.datetime.now()
        status_update_message = f'IMPORTANT Begin processing playlist {playlist["pid"]} at {current_time}'
        send_message(status_update_message, chat_id_dev)
    
    # 50 is the limit for SpotiPy 
    chunk_size = 50
    track_id = 0
    
    for i in range(0, len(track_uris), chunk_size):
        chunk = track_uris[i:i + chunk_size]
        
        artist_genre_chunk = get_artist_genre(chunk, sp)
        
        """
        * NOTE: as of 27/07/23, albums do NOT return any genres. So get_album_genres() removed for now, to reduce spotify API calls
        """
        # album_genre_chunk = get_album_genre(chunk, sp)
        # track_genre_chunk = arr_cleanup(arr_combine(artist_genre_chunk, album_genre_chunk))
        track_genre_chunk = artist_genre_chunk
        
        for genre in track_genre_chunk:
            id = f"{playlist_id}_{track_id}"
            # genre['id'] = id
            genre_list.append(genre)
            track_id += 1

    return genre_list




"""
Retrieves the total number of tracks a user has over each playlist
"""
def get_user_total_tracks(sp):
    user_playlists = get_user_playlists(sp)
    total_track_count = 0
    for playlist in user_playlists:
        total_track_count += playlist['playlist_track_count']
    return total_track_count



"""

"""
def get_playlist_top_tracks(sp, playlist_uri, track_count = 10, time_range = 'long_term'):
    valid_time_ranges = ['short_term', 'medium_term', 'long_term']
    if time_range not in valid_time_ranges:
        raise ValueError('Value of range must be short_term (4 weeks), medium_term (6 months) or long_term (all time)')
    
    playlist_tracks = get_playlist_tracks(sp, playlist_uri)['tracks']
    playlist_tracks_uris = [track['track_uri'] for track in playlist_tracks]
    playlist_top_tracks = []
    
    user_top_tracks = []
    user_top_tracks.extend(get_user_top_tracks(sp, offset=0, time_range=time_range))
    user_top_tracks.extend(get_user_top_tracks(sp, offset=50, time_range=time_range))
        
    for track in user_top_tracks:
        if track['track_uri'] in playlist_tracks_uris and len(playlist_top_tracks) < track_count:
            playlist_top_tracks.append(track)
            if len(playlist_top_tracks) == track_count:
                break
    
    print(len(playlist_top_tracks))
    return playlist_top_tracks



"""
Takes the user's playlists and their track counts, along with the top tracks of the user, and calculates the popularity of each playlist based on the number of top tracks present in them.
"""
def get_user_playlist_popularity(sp):
    playlists = get_user_playlists(sp)
    playlist_count = get_user_playlist_count(sp)
    
    playlist_details = [{
        'uri' : playlist['playlist_uri'],
        'title': playlist['playlist_name'],
        'href': playlist['playlist_href'],    
        'track_count': playlist['playlist_track_count']    
    } for playlist in playlists]
    
    top_tracks = get_user_top_tracks(sp, limit=100)
    playlist_popularity = []
    
    for idx, playlist in enumerate(playlist_details, start=1):
        
        status_message = f'Analysing Playlist {idx}/{playlist_count}'
        print(status_message)
        if(idx == playlist_count): print(' ')
        
        tracks = get_playlist_tracks(sp, playlist['uri'])

        popularity_score = sum(1 for track in tracks['tracks'] if track['track_uri'] in [t['track_uri'] for t in top_tracks])
        popularity_percentage = round((popularity_score / playlist['track_count'] * 100), 2)

        playlist_popularity.append({
            'title': playlist['title'],
            'popularity': popularity_score,
            'popularity_percentage': popularity_percentage,
            'href': playlist['href'],
            'uri': playlist['uri'],
        })
        
    other_playlist_popularity = {
        'title': 'Other',
        'popularity': 100 - sum(p['popularity'] for p in playlist_popularity),
        'popularity_percentage': 'N/A',
        'href': 'N/A',
        'uri': 'N/A',
    }
    
    playlist_popularity.append(other_playlist_popularity)

    playlist_popularity.sort(key=lambda x: x['popularity'], reverse=True)

    for playlist in playlist_popularity:
        playlist['popularity'] = str(playlist['popularity']) + '%'
        playlist['popularity_percentage'] = str(playlist['popularity_percentage']) + '%'

    return playlist_popularity



"""

"""
def get_user_top_tracks_for_artist(sp, artist, top_track_count=5, time_range='long_term', track_source_count=100):
    
    valid_time_ranges = ['short_term', 'medium_term', 'long_term']
    if time_range not in valid_time_ranges:
        raise ValueError('Value of range must be short_term (4 weeks), medium_term (6 months) or long_term (all time)')
    if top_track_count > 100 or track_source_count > 100:
        raise ValueError('Maximum value for track_count is 100')
    
    tracks = [track for track in get_user_top_tracks(sp, track_source_count, time_range) if track['artist']==artist][:top_track_count]
    return tracks
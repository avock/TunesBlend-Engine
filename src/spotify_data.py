import datetime, pprint

from src.data_processing import *
from src.telegram_bot import *


"""
Spotify Constants
"""
genre_list = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']

def get_audio_features(track_uris, sp):
    audio_features = sp.audio_features(track_uris)
    filtered_audio_features = [filter_audio_feature(audio_feature) for audio_feature in audio_features]
    return filtered_audio_features

"""
Function to retreive the genre(s) of the album for one or multiple tracks.
"""
def get_album_genre(track_uris, sp):
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
def get_artist_genre(track_uris, sp):
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
Returns an array of playlists in the following format:
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
Returns an array of tracks in the following format:
    ```
    {
        'track_rank': 1,
        'track_name': 'Alone',
        'track_uri': 'spotify:track:3MEYFivt6bilQ9q9mFWZ4g',
        'track_href': 'https://open.spotify.com/track/3MEYFivt6bilQ9q9mFWZ4g',
        'artist': 'Marshmello',
        'artist_uri': 'spotify:artist:64KEffDW9EtZ1y2vBYgq8T',
        'album': 'Alone',
        'album_uri': 'spotify:album:7ePC9qS9mSOTY9E0YPP6yg'
    }
    ```
"""
def get_user_top_tracks(sp, limit=50, offset=0, time_range='long_term'):
    valid_time_ranges = ['short_term', 'medium_term', 'long_term']
    if time_range not in valid_time_ranges:
        raise ValueError('Value of range must be short_term (4 weeks), medium_term (6 months) or long_term (all time)')
    
    if limit > 50:
        raise ValueError('Value of limit must be less than 50')
    
    top_tracks = []
    try:
        track_list = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)['items']
        
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

"""
def get_spotify_recommendation(sp, limit=10, seed_artists=None, seed_genres=None, seed_tracks=None, country=None, **kwargs):
    cleaned_recommended_tracks = []
    
    audio_features = ['danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
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
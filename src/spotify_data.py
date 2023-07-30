import datetime, pprint

from src.data_processing import *
from src.telegram_bot import *
from src.spotify_utils import *



"""
Spotify Constants
"""
genre_list = ['acoustic', 'afrobeat', 'alt-rock', 'alternative', 'ambient', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'brazil', 'breakbeat', 'british', 'cantopop', 'chicago-house', 'children', 'chill', 'classical', 'club', 'comedy', 'country', 'dance', 'dancehall', 'death-metal', 'deep-house', 'detroit-techno', 'disco', 'disney', 'drum-and-bass', 'dub', 'dubstep', 'edm', 'electro', 'electronic', 'emo', 'folk', 'forro', 'french', 'funk', 'garage', 'german', 'gospel', 'goth', 'grindcore', 'groove', 'grunge', 'guitar', 'happy', 'hard-rock', 'hardcore', 'hardstyle', 'heavy-metal', 'hip-hop', 'holidays', 'honky-tonk', 'house', 'idm', 'indian', 'indie', 'indie-pop', 'industrial', 'iranian', 'j-dance', 'j-idol', 'j-pop', 'j-rock', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'malay', 'mandopop', 'metal', 'metal-misc', 'metalcore', 'minimal-techno', 'movies', 'mpb', 'new-age', 'new-release', 'opera', 'pagode', 'party', 'philippines-opm', 'piano', 'pop', 'pop-film', 'post-dubstep', 'power-pop', 'progressive-house', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'rainy-day', 'reggae', 'reggaeton', 'road-trip', 'rock', 'rock-n-roll', 'rockabilly', 'romance', 'sad', 'salsa', 'samba', 'sertanejo', 'show-tunes', 'singer-songwriter', 'ska', 'sleep', 'songwriter', 'soul', 'soundtracks', 'spanish', 'study', 'summer', 'swedish', 'synth-pop', 'tango', 'techno', 'trance', 'trip-hop', 'turkish', 'work-out', 'world-music']



"""
Function to retrieve audio_features of a track

"""
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

def get_user_playlists(sp):
    playlists = sp.current_user_playlists()['items']
    playlist_list = []
    for playlist in playlists:
        playlist_detail = {
            'playlist_name' : playlist['name'],
            'playlist_id': playlist['id'],
            'playlist_track_count': playlist['tracks']['total']
        }
        playlist_list.append(playlist_detail)
    
    return playlist_list


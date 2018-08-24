# from spotipy import oauth2
from spotipy import util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy

user_library_read = 'user-library-read'
playlist_modify_public = 'playlist-modify-public'
scope = user_library_read + ' ' + playlist_modify_public
user = 'ar15student'
client_id = '6f0e1625137a45bab876b91906a38f01'
client_secret = 'bc349d6984e140ef98639e1c77e8ba0b'

token = util.prompt_for_user_token(user,scope=scope,client_id=client_id,client_secret=client_secret, redirect_uri='http://localhost/')
spotify = spotipy.Spotify(auth=token)

library = {}
def extract_library():
    library_results = spotify.current_user_saved_tracks(limit=50, offset=0)
    extract_artist_song(library_results)
    offset = 50
    while len(library_results['items']) != 0:
        library_results = spotify.current_user_saved_tracks(limit=50, offset=offset)
        extract_artist_song(library_results)
        offset += 50
def extract_artist_song(response):
    for i in range(len(response['items'])):
        song_id = response['items'][i]['track']['id']
        song = response['items'][i]['track']['name']
        library[song] = song_id
def clean_playlists():
    # I am going to assume you don't have more than 50 playlists unless you are a madman.
    playlists = spotify.current_user_playlists(limit=50)
    playlist_ids = []
    for playlist in playlists['items']:
        print('id: ', playlist['id'])
        print('name: ', playlist['name'])
        playlist_ids.append(playlist['id'])
    num_playlists = len(playlist_ids)
    for i in range(num_playlists):
        song_ids = []
        results = spotify.user_playlist_tracks(user, playlist_id=playlist_ids[i], limit=100)
        for dic in results['items']:                              
            song_id = dic['track']['id']
            song_name = dic['track']['name']
            print(song_id + ', ' + song_name)
            if song_name not in library:
                song_ids.append(song_id)
        print(song_ids)
        if len(song_ids) != 0:
            spotify.user_playlist_remove_all_occurrences_of_tracks(user, playlist_id=playlist_ids[i], tracks=song_ids)
        print(song_ids)
extract_library()
clean_playlists()

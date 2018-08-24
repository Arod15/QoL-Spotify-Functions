from spotipy import util
# from spotipy.oauth2 import SpotifyClientCredentials
# from spotipy.oauth2 import SpotifyOAuth
import spotipy
import config

token = util.prompt_for_user_token(config.user,scope=config.scope,client_id=config.client_id,client_secret=config.client_secret, redirect_uri='http://localhost/')
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
    song_batch_len = len(response['items'])
    for i in range(song_batch_len):
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
        results = spotify.user_playlist_tracks(config.user, playlist_id=playlist_ids[i], limit=100)
        for dic in results['items']:                              
            song_id = dic['track']['id']
            song_name = dic['track']['name']
            print(song_id + ', ' + song_name)
            if song_name not in library:
                song_ids.append(song_id)
        print(song_ids)
        if len(song_ids) != 0:
            spotify.user_playlist_remove_all_occurrences_of_tracks(config.user, playlist_id=playlist_ids[i], tracks=song_ids)
        print(song_ids)
extract_library()
clean_playlists()

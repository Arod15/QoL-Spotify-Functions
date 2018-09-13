from spotipy import util
import spotipy
import config
import requests

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
        artist = response['items'][i]['track']['artists'][0]['name']
        artist_id = response['items'][i]['track']['artists'][0]['id']
        library[song] = [song_id, artist, artist_id]
# remove all songs found in playlists that are not found in your library
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
        if len(song_ids) != 0:
            spotify.user_playlist_remove_all_occurrences_of_tracks(config.user, playlist_id=playlist_ids[i], tracks=song_ids)
# create a playlist of many songs from artists you would like to listen to
def top_songs_from_artist_library(artists):
    for artist in artists:
        top_songs = spotify.artist_top_tracks(str(artist))['items']['track']['id']
        print(top_songs)
        break
    return []
def retrieve_artists_library():
    artists = {}
    for key in library:
        artists[library[key][2]] = 0
    return artists
def artists_song_dump_playlist():
    all_playlists = spotify.current_user_playlists()
    all_playlists = all_playlists['items']
    
    found = False
    dump_id = ''

    for playlist in all_playlists:
        if found:
            break
        if playlist['name'] == 'Song Dump':
            found = True
            dump_id = playlist['id']

    if not found:
        # create the playlist and find the id
        spotify.user_playlist_create(config.user, 'Song Dump', public=True)
        for playlist in all_playlists:
            if playlist['name'] == 'Song Dump':
                dump_id = playlist['id']
    all_artists = retrieve_artists_library()
    dump_songs = top_songs_from_artist_library(all_artists)
    print(dump_songs)
    # spotify.user_playlist_add_tracks(user=config.user, playlist_id=dump_id, tracks=dump_songs, position=None)
extract_library()
print(library)
artists_song_dump_playlist()
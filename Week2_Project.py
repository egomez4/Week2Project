import requests
import json

song_artist = (input('Enter Artist Name: '))
song_title = (input('Enter name of song: '))

def song_search(song_artist, song_title):
    key = "d01d05bd4c4b77d9143f319216a6342b"
    url = 'http://api.musixmatch.com/ws/1.1/track.search?'
    parameters = {'apikey': key, 'q_track': song_title, 'q_artist': song_artist}
    response = requests.get(url, params = parameters)
    song = response.json()

    track_id = song['message']['body']['track_list'][0]['track']['track_id']
    commontrack_id = song['message']['body']['track_list'][0]['track']['commontrack_id']
    
    return track_id


def get_lyrics(track_id):    
track_id = song['message']['body']['track_list'][0]['track']['track_id']
lyrics_url = f'http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey={key}&track_id={track_id}'
lyrics = requests.get(lyrics_url)
print(lyrics.status_code)
lyrics_data = lyrics.json()
lyrics_body = lyrics_data['message']['body']['lyrics']['lyrics_body']
print(lyrics_body)
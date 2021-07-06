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
    return (track_id)


def get_lyrics(track_id):  
    key = "d01d05bd4c4b77d9143f319216a6342b"
    lyrics_url = f'http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey={key}&track_id={track_id}'
    lyrics = requests.get(lyrics_url)
    lyrics_data = lyrics.json()
    lyrics_body = str(lyrics_data['message']['body']['lyrics']['lyrics_body'])
    
    return (lyrics_body)

def sentiment (lyrics):
    sentiment_url = 'http://text-processing.com/api/sentiment/'
    options = { 'text' : lyrics}
    response = requests.post(sentiment_url, data = options)
    sentiment = response.json()
    sentiment
    return sentiment


try:
    song_id = song_search(song_artist, song_title)
    lyrics = get_lyrics(song_id)
    song_analysis = sentiment(lyrics)
    print(song_analysis)

except TypeError as e:
    print('Error: Lyrics are Unavailable')
import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def song_search(song_artist, song_title):
    key = "d01d05bd4c4b77d9143f319216a6342b"
    url = 'http://api.musixmatch.com/ws/1.1/track.search?'
    parameters = {'apikey': key, 'q_track': song_title, 'q_artist': song_artist}
    response = requests.get(url, params=parameters)
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


def sentiment(lyrics):
    sentiment_url = 'http://text-processing.com/api/sentiment/'
    options = {'text': lyrics}
    response = requests.post(sentiment_url, data=options)
    sentiment = response.json()
    return sentiment

def main():
    is_using_system = True
    # generate UI
    while is_using_system:
        print('------------------------')
        print('MUSIC SENTIMENT ANALYZER')
        print('------------------------')

        # ask user what they would like to do
        print('1. Perform sentiment analysis on a song')
        print('2. Compare the polarity of two songs')
        print('3. Quit')
        user_input = int(input('Select an option:'))


        # option 1
        if user_input == 1:
            print('-------------')
            print('SONG ANALYSIS')
            print('-------------')

            # get song id
            song_artist = (input('Enter Artist Name: '))
            song_title = (input('Enter name of song: '))
            song_id = song_search(song_artist, song_title)

            # get song lyrics
            lyrics = get_lyrics(song_id)

            # perform sentiment analysis
            analysis = sentiment(lyrics)

            # create visualization
            #
            organized_analysis = dict(positive={'value': analysis['probability']['pos']},
                         negative={'value': analysis['probability']['neg']},
                         neutral={'value': analysis['probability']['neutral']},
                         song_name=song_title,
                         artist=song_artist,
                         overall_polarity=analysis['label']
                         )
            df = pd.DataFrame.from_dict(organized_analysis)
            print(df)
            x = ['Positive', 'Negative', 'Neutral']
            y = [analysis['probability']['pos'], analysis['probability']['neg'], analysis['probability']['neutral']]
            plt.bar(x, y)
            plt.title('Polarity of ' + song_title + ' by ' + song_artist)
            plt.ylabel('Sentiment Score')
            plt.show()

            # prompt user if they would like to save the analysis to the database
            # code that saves dataframe to database
            is_using_system = False


if __name__ == "__main__":
    main()
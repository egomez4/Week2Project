import requests
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


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
        try:
            print('\n------------------------')
            print('MUSIC SENTIMENT ANALYZER')
            print('------------------------')

            # ask user what they would like to do
            print('1. Perform sentiment analysis on a song')
            print('2. Compare the polarity of two songs')
            print('3. Quit')
            print('')  # white space
            user_input = int(input('Select an option: '))
            print('')

            # option 1
            if user_input == 1:
                try:
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
                    print(f'\nPerforming sentiment analysis on {song_title} by {song_artist}.')

                    # make bar chart
                    pos = analysis['probability']['pos']
                    neg = analysis['probability']['neg']
                    neutral = analysis['probability']['neutral']

                    # bar axes
                    x = ['Positive', 'Negative', 'Neutral']
                    y = [pos, neg, neutral]

                    df = pd.DataFrame(list(zip(x, y)), columns=['polarity', 'value'])
                    print(df)
                    fig = px.bar(df, x='polarity',
                                 y='value',
                                 title=f'Polarity of {song_title} by {song_artist}'
                                 )
                    # show chart to user
                    print('\nAnalysis complete. The produced visualization will appear in a new window.')

                    # write to html
                    fig.write_html('songSentimentAnalysis.html')
                    print('\nReturning to main menu.')
                except TypeError as e:
                    print('Lyrics not found')

            # option 2
            if user_input == 2:
                try:
                    # generate UI
                    print('-------------------------')
                    print('SONG SENTIMENT COMPARISON')
                    print('-------------------------')

                    # get song ids
                    song1_artist = input('Enter an artist for the first song: ')
                    song1_title = input('Enter the name of the first song: ')
                    song1_id = song_search(song1_artist, song1_title)

                    song2_artist = input('Enter an artist for the second song: ')
                    song2_title = input('Enter the name of the second song: ')
                    song2_id = song_search(song2_artist, song2_title)

                    # get lyrics
                    song1_lyrics = get_lyrics(song1_id)
                    song2_lyrics = get_lyrics(song2_id)

                    # perform sentiment analysis
                    song1_analysis = sentiment(song1_lyrics)
                    song2_analysis = sentiment(song2_lyrics)
                    print(f'\nComparing {song1_title} by {song1_artist} and {song2_title} by {song2_artist}')

                    # make stacked bar chart
                    barchart = go.Figure(data=[go.Bar(
                        name=f'{song1_title} by {song1_artist}',
                        x=['Positive', 'Negative', 'Neutral'],
                        y=[song1_analysis['probability']['pos'],
                           song1_analysis['probability']['neg'],
                           song1_analysis['probability']['neutral']
                           ]
                    ), go.Bar(
                        name=f'{song2_title} by {song2_artist}',
                        x=['Positive', 'Negative', 'Neutral'],
                        y=[song2_analysis['probability']['pos'],
                           song2_analysis['probability']['neg'],
                           song2_analysis['probability']['neutral']
                           ]
                    )
                    ])
                    barchart.update_layout(barmode='stack')
                    print('\nComparison Completed, open generated html file to view visualization.')
                    print('\nReturning to main menu.')
                    barchart.write_html('songComparison.html')
                except TypeError:
                    print('Lyrics to one or both songs not found.')

            # option 3
            if user_input == 3:
                user_quit = input('Would you like to quit? (y/n) ')
                if user_quit == 'y':
                    print('Goodbye.')
                    is_using_system = False
                elif user_quit == 'n' or 'N':
                    print('\nReturning to main menu.')
        except ValueError as e:
            print('Error: Please enter a number.')


if __name__ == "__main__":
    main()

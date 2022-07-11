# import relevant libraries
import pandas as pd
import requests
import json
import os
import re

# specifying the ncoding is important!
with open("WhatsApp Chat with Sugar Mummy SweetPea.txt", mode = 'r', encoding='utf8') as f:
    lines = f.readlines()


# convert lines to pandas dataframe
lines_df = pd.DataFrame(lines)
# rename column to "data"
lines_df.columns = ['data']
# split 'data' column on first occurence of "-" and expand into two columns, 'timestamp' and 'text'
lines_df[['timestamp', 'text']] = lines_df['data'].str.split('-', n=1, expand=True)
# split 'text' column on first occurence of ":" and expand into two columns, 'speaker' and 'text'
lines_df[['speaker', 'messages']] = lines_df['text'].str.split(':', n=1, expand=True)


# filter only messages that contain a spotify track URL
spotify_links = lines_df.text[lines_df['messages'].str.contains('https://open.spotify.com/track/', na=False)].reset_index()
# join all the rows into one string for regex search
spotify_uris = ''.join(spotify_links['text'])
# replace all http with spotify syntax for uri
spotify_uris = re.sub('https://open.spotify.com/track/', 'spotify:track:', string=spotify_uris)
# exctract uri with spotify IDs alone
spotify_uris = re.findall('spotify:track:[A-Za-z0-9]+', string=spotify_uris)

# Spotify!


# set environment variables, ensure to delete after running once or use command line
os.environ['SPOTIFY_USER_ID'] = "YOUR SPOTIFY USERNAME"
os.environ['SPOTIFY_TOKEN'] = "YOUR GENERATED TOKEN"

# retrieve environment variables
SPOTIFY_USER_ID = os.getenv("SPOTIFY_USER_ID")
SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")



# define the create playlist funtion
def create_playlist():
    '''
    This function connects to the Spotify API using your Auth Token and creates a new playlist for your user ID as specified
    by you in the query and request_body
    '''
    request_body = json.dumps(
        {
            "name": "SweetPea x KP Love Jams",
            "description": "Songs that made us think of each other with warmed and melted hearts",
            "public": True,
        }
    )

    query = "https://api.spotify.com/v1/users/{}/playlists".format(SPOTIFY_USER_ID)

    response = requests.post(
        query,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SPOTIFY_TOKEN),
        },
    )
    return response.json()

# call the create_playlist function
res = create_playlist()
# extract playlist id
playlist_id = res["id"]


# # Add songs to playlist


def add_songs(playlist_id, uris):
    """
    Add all songs into the new Spotify playlist
    """
  
    request_data = json.dumps(uris)
    query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
        playlist_id)
  
    response = requests.post(
        query,
        data=request_data,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(SPOTIFY_TOKEN),
        },
    )
    return response

# call the add_songs_ function
add_songs(playlist_id, spotify_uris)
# Libraries import
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from itertools import zip_longest

# Group a bunch of items
def grouper(iterable, n=2, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

# Spotify object
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# Read dataset
df = pd.read_csv('../dataset/data.csv')

ids = df['id']

# print(type(ids))

# ids = list(ids)
# print(type(ids))
# print(ids)

#print(ids.head())

# print(ids[0,0])
for idd in grouper(ids):
    res = spotify.tracks(idd)
    # print(res)
    album_ids = [""]*len(idd)
    for i in range(len(idd)):
        album_ids[i] = res['tracks'][i]['album']['id']
        print(album_ids[i])
    res_al = spotify.albums(album_ids)
    print(res_al['albums'][0])    
    break

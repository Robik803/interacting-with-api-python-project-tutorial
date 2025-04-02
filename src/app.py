import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import matplotlib.pyplot as plt


# load the .env file variables
load_dotenv()

# Setting the environment variables
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
scope = os.getenv('SCOPE') # 'user-library-read'
redirect_uri = os.getenv('REDIRECT_URI') # 'http://localhost:8888/callback'

# Connection to the Spotify API

if not client_id or not client_secret:
    raise ValueError("Please set the CLIENT_ID and CLIENT_SECRET environment variables.")

spotify = spotipy.Spotify(auth_manager= SpotifyClientCredentials(client_id = client_id,
                                                                    client_secret = client_secret))

# Getting the top tracks of an artist

artist_id = os.getenv('ARTIST_ID')
top_tracks = spotify.artist_top_tracks(artist_id = artist_id, country = "US")
tracks = [ {'name': track['name'], 'popularity': track['popularity'], 'duration': track['duration_ms'] / 60000 } for track in top_tracks['tracks']]

# Transform the data into a Pandas Dataframe

df = pd.DataFrame(tracks)
df["duration"] = df["duration"].round(2)
print(df.sort_values(by = "popularity", ascending=False).head(3))

# Duration/Popularity correlation

plt.figure(figsize=(9, 6))
plt.scatter(df['popularity'], df['duration'])
plt.show()

if df['popularity'].corr(df['duration']) > 0.5:
    print('There is a positive correlation between popularity and duration of the songs')
else:
    print('It doesn\'t exist a statistical relationship between popularity and duration of the songs')

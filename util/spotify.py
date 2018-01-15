import requests
import base64
import json
import random

SPOTIFY_CLIENT_ID = "9b4b1e609652443b8743e95b15122284"
SPOTIFY_CLIENT_SECRET = "372840ae3ccd4e25b70776529bdc73e8"
ACCESS_TOKEN = ""
'''
Gets Access Token
'''
def get_access_token():
    print "Getting Spotify Token..."
    url = "https://accounts.spotify.com/api/token"
    body_params = {"grant_type": "client_credentials"}
    response = json.loads(requests.post(url, data=body_params, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)).text)
    global ACCESS_TOKEN
    ACCESS_TOKEN = response["access_token"]

'''
Takes in genre (all lowercase), danceability(0.0 to 1.0), and energy(0.0 to 1.0)
Chooses a random song that fits the requirements
Returns a URI to embed that song on the webpage using iframe
'''
def get_song(genre, energy):
    global ACCESS_TOKEN
    if ACCESS_TOKEN == "":
        get_access_token()
    url = "https://api.spotify.com/v1/recommendations?limit=10&market=US&seed_genres=" + genre + "&target_energy=" + str(energy)
    headers = {"Authorization":("Bearer " + ACCESS_TOKEN), "Accept": "application/json", "Content-Type": "application/json"}
    response = json.loads(requests.get(url, headers=headers).text)
    tracks = response["tracks"]
    track = random.choice(tracks)
    #iframe = '<iframe src="' + track["uri"] + '" width="300" height="380" frameborder="0" allowtransparency="true"></iframe>'
    return track["uri"]

#print get_song("pop", .25)

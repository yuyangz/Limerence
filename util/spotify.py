from __future__ import print_function
import requests
import base64
import json
import random
import keys


SPOTIFY_CLIENT_ID = ""
SPOTIFY_CLIENT_SECRET = ""
ACCESS_TOKEN = ""


def get_access_token():
    """Gets Access Token"""
    global SPOTIFY_CLIENT_ID
    global SPOTIFY_CLIENT_SECRET
    global ACCESS_TOKEN

    if SPOTIFY_CLIENT_ID == "" or SPOTIFY_CLIENT_SECRET == "":
        spotkeys = keys.get_key("spotify")
        SPOTIFY_CLIENT_ID = spotkeys[0]
        SPOTIFY_CLIENT_SECRET = spotkeys[1]

    print("Getting Spotify Token...")
    url = "https://accounts.spotify.com/api/token"
    body_params = {"grant_type": "client_credentials"}
    response = json.loads(requests.post(url, data=body_params, auth=(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)).text)

    ACCESS_TOKEN = response["access_token"]

'''
Takes in genre (all lowercase), danceability(0.0 to 1.0), and energy(0.0 to 1.0)
Chooses a random song that fits the requirements
Returns a URI to embed that song on the webpage using iframe
'''
def get_song(genre, energy, is_rand):
    global ACCESS_TOKEN
    if ACCESS_TOKEN == "":
        get_access_token()
    url = "https://api.spotify.com/v1/recommendations?limit=10&market=US&seed_genres=" + genre + "&target_energy=" + str(energy)
    headers = {"Authorization":("Bearer " + ACCESS_TOKEN), "Accept": "application/json", "Content-Type": "application/json"}
    response = json.loads(requests.get(url, headers=headers).text)
    tracks = response["tracks"]
    if is_rand:
        track = random.choice(tracks)
        return track["uri"]
    else:
        uri_list = []
        for track in tracks:
            uri_list.append(track["uri"])
        return uri_list
    #iframe = '<iframe src="' + track["uri"] + '" width="300" height="380" frameborder="0" allowtransparency="true"></iframe>'

#print get_song("pop", .25)

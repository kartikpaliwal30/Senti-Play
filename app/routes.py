from flask import Flask, redirect, render_template
from flask import request
import base64, requests, json
from app import app
import urllib
from urllib.parse import quote 
import pandas as pd
#  Client Keys
CLIENT_ID = "ce1e57d2805d4757bffa9489344f68b4"
CLIENT_SECRET = "2cec65dc1ccc4778bfa16d36c56c1169"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1:5000/"
REDIRECT_URI = "http://127.0.0.1:5000/spotify_sentiment_analysis"
SCOPE = 'user-read-private user-read-playback-state user-modify-playback-state user-library-read'
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}

@app.route('/spotify_sentiment_analysis_login')
def spotify():
    return render_template('spotify_sentiment_analysis_login.html')

@app.route('/spotify_authentication')
def spotify_auth():
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)
 
@app.route('/spotify_sentiment_analysis')
def spotify_sentiment_analysis():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET).encode())
    headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)
    
    print(profile_data)

    # # Get user playlist data
    # playlist_api_endpoint = "{}/tracks".format(user_profile_api_endpoint)
    # playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)

    # playlist_data = playlists_response.text
    # playlist_data = playlist_data[83:-142]
    # playlist_data = json.loads(playlist_data)

    # playlist_list = []

    # for i in playlist_data:
    #     tmp = [i['added_at'][:-10], 
    #             i['track']['name'], 
    #             i['track']['artists'][0]['name'], 
    #             i['track']['album']['images'][0]['url'],
    #             i['track']['external_urls']['spotify'],
    #             i['track']['id']]
    #     playlist_list.append(tmp)

    # playlist_df = pd.DataFrame(playlist_list, columns=['Date', 'Track_Name', 'Artist', 'Cover_Image', 'URL', 'Track_ID'])


    return render_template('spotify_sentiment_analysis.html')
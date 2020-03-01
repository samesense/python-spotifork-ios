# python-spotifork

Create an iOS shortcut for `spotipy_oauth_demo.py` in pythonista to use. You also need a yaml file in this folder. It contains credentials for your app from Spotify. Pythonista's `requests` library is old, so I had to include and modify the `spotipy` library to get it working. It was cloned from github on 2020 Feb 28.

### config.yaml
```
username: "samesense"
client_id: "GET FROM SPOFITY"
client_secret: "GET FROM SPOTIFY"
redirect_uri: "http://localhost:8080"
```

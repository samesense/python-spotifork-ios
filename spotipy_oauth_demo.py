# https://github.com/plamere/spotipy/blob/master/spotipy/util.py
# http://www.acmesystems.it/python_httpd

from bottle import route, run, request
import spotipy
import sys
import spotifork
import appex
from spotipy import oauth2

PORT_NUMBER = 8080
SPOTIPY_REDIRECT_URI = "http://localhost:8080"
SCOPE = "user-library-read,playlist-modify-public"
CACHE = ".spotipyoauthcache"

user_config = spotifork.load_config()
SPOTIPY_CLIENT_ID = user_config["client_id"]
SPOTIPY_CLIENT_SECRET = user_config["client_secret"]

sp_oauth = oauth2.SpotifyOAuth(
	SPOTIPY_CLIENT_ID,
	SPOTIPY_CLIENT_SECRET,
	SPOTIPY_REDIRECT_URI,
	scope=SCOPE,
	cache_path=CACHE, )


@route("/")
def index():
	access_token = ""

	token_info = sp_oauth.get_cached_token()

	if token_info:
		print("Found cached token!")
		access_token = token_info["access_token"]
	else:
		url = request.url
		code = sp_oauth.parse_response_code(url)
		if code:
			token_info = sp_oauth.get_access_token(code)
			access_token = token_info["access_token"]

	if access_token:
		sp = spotipy.Spotify(auth=access_token)
		#results = sp.current_user()
		url = appex.get_url()
		id = url.split('/')[-1].split('?')[0]
		print(url, id)
		playlist_id = f"spotify:playlist:{id}"
		username = user_config["username"]
		playlist = sp.playlist(playlist_id)
		results = spotifork.get_tracks(sp, playlist["id"])
		spotifork.write_tracks(sp, username, playlist, results)
		sys.stderr.close()
		return results

	else:
		return htmlForLoginButton()


def htmlForLoginButton():
	auth_url = getSPOauthURI()
	htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
	return htmlLoginButton


def getSPOauthURI():
	auth_url = sp_oauth.get_authorize_url()
	return auth_url


run(host="", port=8080)


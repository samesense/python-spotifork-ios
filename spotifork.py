import sys
import spotipy
import yaml
import spotipy.util as util
import pprint


def load_config():
    stream = open("config.yaml")
    user_config = yaml.load(stream)
    #pprint.pprint(user_config)
    return user_config


def show_tracks(tracks):
    for i, item in enumerate(tracks["items"]):
        track = item["track"]
        print("   %d %32.32s %s" % (i, track["artists"][0]["name"], track["name"]))


def get_tracks(sp, playlist_id):
    t = sp.playlist_tracks(playlist_id, fields="items.track.id,items.track.name,total")
    pprint.pprint(t)
    results = [d["track"]["id"] for d in t["items"]]
    return results


def write_tracks(sp, username, base_playlist, tracks):
    playlist = sp.user_playlist_create(
        username,
        f"{base_playlist['name']} FORK",
        description=f"Fork; {base_playlist['description']}",
    )
    #pprint.pprint(playlist)
    results = sp.user_playlist_add_tracks(username, playlist["id"], tracks)
    # pprint.pprint(results)


if __name__ == "__main__":
    global sp
    global user_config
    load_config()
    token = util.prompt_for_user_token(
        user_config["username"],
        scope="playlist-modify-public",
        client_id=user_config["client_id"],
        client_secret=user_config["client_secret"],
        redirect_uri=user_config["redirect_uri"],
    )
    username = user_config["username"]
    sp = spotipy.Spotify(auth=token)

    playlist_id = "spotify:playlist:XXXX"
    playlist = sp.playlist(playlist_id)
    results = get_tracks(playlist["id"])
    write_tracks(sp, username, playlist, results)

    # print(results)
    # tracks = results["tracks"]
    # show_tracks(tracks)
    # while tracks["next"]:
    #     tracks = sp.next(tracks)
    #     show_tracks(tracks)
# spotify:playlist:1If5PrwyZWpET11UE1LPVu

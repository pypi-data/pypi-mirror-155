#!/usr/bin/env python
import os
from rich import print

from main import auth_manager, spotipy
auth_manager.scope = "user-read-currently-playing user-library-modify"

sp = spotipy.Spotify(auth_manager=auth_manager)
# track = sp.current_user_playing_track()
# token = auth_manager.get_cached_token()
# access_token = token["access_token"]

# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json",
# }
# BASE_URL = "https://api.spotify.com/v1/"


track = sp.currently_playing()["item"]

track_id = track["id"]
image = track["album"]["images"][0]["url"]
name = track["name"]
artists_names = ", ".join(map(lambda a: a["name"], track["artists"]))

sp.current_user_saved_tracks_delete(tracks=[track_id])

os.system(f"curl -so /tmp/spimage {image}")
message = f"♡ {artists_names} - {name}"
cmd = f'notify-send -i /tmp/spimage "{message}"'
print(message)
os.system(cmd)

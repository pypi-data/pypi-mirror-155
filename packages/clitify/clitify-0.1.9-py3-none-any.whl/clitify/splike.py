#!/usr/bin/env python
"""Like a music to spotify.
More precisely add the music currently listened to, to the user library.
"""
import os
import spotipy
from rich import print

import argparse

from main import spotipy, auth_manager

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

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-o", "--output", type=bool, default=True, help="Return stdout")
parser.add_argument("-n", "--notify", type=bool, default=True, help="Send a notification")


def main(*args):

    parsed = parser.parse_args(args)

    track = sp.currently_playing()["item"]

    track_id = track["id"]
    image = track["album"]["images"][0]["url"]
    name = track["name"]
    artists_names = ", ".join(map(lambda a: a["name"], track["artists"]))

    sp.current_user_saved_tracks_add(tracks=[track_id])

    os.system(f"curl -so /tmp/spimage {image}")
    message = f"❤️ {artists_names} - {name}"
    cmd = f'notify-send -i /tmp/spimage "{message}"'

    if parsed.output:
        print(message)
    if parsed.notify:
        os.system(cmd)

if __name__ == "__main__":
    main()

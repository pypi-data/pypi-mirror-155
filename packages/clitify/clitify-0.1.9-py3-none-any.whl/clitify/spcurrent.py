#!/usr/bin/env python
"""
Show information about the spotify user.
"""

from main import auth_manager, spotipy

auth_manager.scope = "user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=auth_manager)

track = sp.currently_playing()["item"]

track_id = track["id"]
image = track["album"]["images"][0]["url"]
name = track["name"]
artists_names = ", ".join(map(lambda a: a["name"], track["artists"]))
message = f"{artists_names} - {name}"
print(message)

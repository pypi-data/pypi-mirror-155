#!/usr/bin/env python
import os
import sys
import spotipy
import termcolor

duration_s = float(sys.argv[1])
duration_ms = int(duration_s * 1000)

from main import spotipy, auth_manager
auth_manager.scope = (
    "user-read-playback-position user-read-playback-state user-modify-playback-state"
)

sp = spotipy.Spotify(auth_manager=auth_manager)

playback = sp.current_playback()

progress_ms = playback["progress_ms"]
position_ms = progress_ms + duration_ms

sp.seek_track(position_ms)

track = playback["item"]

track_id = track["id"]
image = track["album"]["images"][0]["url"]
name = track["name"]
artists_names = ", ".join(map(lambda a: a["name"], track["artists"]))


if duration_s < 0:
    duration_text = f"﹣{-duration_s}"
else:
    duration_text = f"+{duration_s}"

os.system(f"curl -so /tmp/spimage {image}")

message = f"{duration_text}s {artists_names} - {name}"
cmd = f'notify-send -i /tmp/spimage "{message}" 2> /dev/stdout'
os.system(cmd)

c_message = termcolor.colored(f"{duration_text}s", "yellow")
c_artists_names = termcolor.colored(artists_names, "blue")
c_name = termcolor.colored(name, "green")

colored_message = f"{c_message} {c_artists_names} - {c_name}"
print(colored_message)

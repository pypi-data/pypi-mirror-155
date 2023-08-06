#!/usr/bin/env python
"""
Show information about the spotify user.
"""

import os
import spotipy

client_id = os.environ["SPOTIPY_CLIENT_ID"]
client_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
cache_path = os.path.join(os.environ["XDG_RUNTIME_DIR"], "spotipy-cache")


redirect_uri = "http://localhost:49153/callback/"
# redirect_uri = "http://localhost:8888/callback/"

auth_manager = spotipy.oauth2.SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    cache_path=cache_path,
)

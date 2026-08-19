# spotify.py
import requests

BASE_URL = "https://api.spotify.com/v1"

def _get(token, path, params=None):
    """Send a GET request to the Spotify Web API and return the response."""
    
    response = requests.get(
        f"{BASE_URL}{path}",
        headers={
            "Authorization": f"Bearer {token}",
        },
        params=params,
        timeout=10,
    )

    # Check for rate limiting
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After")
        error_data = response.json()

        if error_data.get("error", {}).get("reason") == "QUOTA_EXCEEDED":
            raise RuntimeError(
                f"Spotify development quota exceeded. "
                f"Retry after approximately {retry_after} seconds."
            )

    response.raise_for_status()
    return response.json()

def search_artist(token, query):
    """Search Spotify for artists matching a query."""

    data = _get(
        token,
        "/search",
        params={
            "q": query,
            "type": "artist",
            "limit": 5,
        },
    )

    return data["artists"]["items"]

def get_artist(token, artist_id):
    """Get artist information from Spotify."""

    return _get(token, f"/artists/{artist_id}")

def get_albums(token, artist_id):
    """Get albums for an artist from Spotify."""

    albums = []
    params = {
        "include_groups": "album,single",
        "limit": 10,
        "offset": 0,
    }

    while True:
        data = _get(
            token,
            f"/artists/{artist_id}/albums",
            params=params
        )

        albums.extend(data["items"])

        if not data.get("next"):
            break
            
        params["offset"] += params["limit"]
    
    return albums

def get_album_tracks(token, album_id):
    """Get tracks for an album from Spotify."""

    tracks = []
    params = {
        "limit": 50,
        "offset": 0,
    }

    while True:
        data = _get(
            token,
            f"/albums/{album_id}/tracks",
            params=params
        )

        tracks.extend(data["items"])

        if not data.get("next"):
            break
            
        params["offset"] += params["limit"]
    
    return tracks


def get_tracks(token, track_ids):
    """Return full Spotify track objects for the given track IDs."""

    tracks = []

    for track_id in track_ids:
        track = _get(
            token,
            f"/tracks/{track_id}",
        )

        tracks.append(track)

    return tracks

def get_top_tracks(token, time_range):
    """Return the user's top tracks for a given time range.
    
    time_range: short_term, medium_term, long_term"""
    
    tracks = []
    params = {
        "time_range": time_range,
        "limit": 50,
        "offset": 0,
    }

    while True:
        data = _get(
            token,
            "/me/top/tracks",
            params=params
        )

        tracks.extend(data["items"])

        if not data.get("next"):
            break
            
        params["offset"] += params["limit"]
    
    return tracks

def get_saved_tracks(token):
    """Return the user's saved tracks."""
    
    tracks = []
    params = {
        "limit": 50,
        "offset": 0,
    }

    while True:
        data = _get(
            token,
            "/me/tracks",
            params=params
        )

        tracks.extend(data["items"])

        if not data.get("next"):
            break
            
        params["offset"] += params["limit"]
    
    return tracks
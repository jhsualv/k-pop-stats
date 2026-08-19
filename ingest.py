# ingest.py
import sys

from db import get_connection
from queries import  get_access_token, upsert_group, upsert_album, upsert_track
from spotify import search_artist, get_artist, get_albums, get_album_tracks, get_tracks

def parse_release_date(album):
    """Return the release date of an album only when Spotify provides day-level precision."""
    if album["release_date_precision"] == "day":
        return album["release_date"]
    
    return None

def first_image_url(item):
    """Return the URL of the first Spotify image, or None if no image exists."""
    images = item.get("images", [])

    if not images:
        return None

    return images[0]["url"]

def choose_artist(token, query):
    """Choose an artist from a search query."""

    artists = search_artist(token, query)

    if not artists:
        raise ValueError("No artists found for query")

    for i, artist in enumerate(artists):
        print(f"{i + 1}. {artist['name']}")
        print(f"   ID: {artist['id']}")
    
    while True:
        choice = input("\nSelect an artist (1-5): ")

        try:
            index = int(choice) - 1
        except ValueError:
            print("Please enter a number.")
            continue

        if 0 <= index < len(artists):
            return artists[index]

        print(f"Please choose a number between 1 and {len(artists)}.")

def ingest_group(token, artist_id, conn):
    """Fetch a Spotify artist and store it as a group."""

    artist = get_artist(token, artist_id)
    
    spotify_artist_id = artist["id"]
    name = artist["name"]
    profile_image = first_image_url(artist)

    print(f"Ingesting {name}...")

    group_id = upsert_group(name, spotify_artist_id, profile_image, conn)
    
    print(f"Group ID: {group_id}")

    ingest_albums(
        token,
        spotify_artist_id,
        group_id,
        conn,
    )

    return group_id

def ingest_albums(token, spotify_artist_id, group_id, conn):
    """Fetch albums for an artist and store them."""
    albums = get_albums(token, spotify_artist_id)

    print(f"Found {len(albums)} albums/singles.")

    for album in albums:
        name = album["name"]
        spotify_album_id = album["id"]
        album_type = album["album_type"]
        release_date = parse_release_date(album)
        image_url = first_image_url(album)
        
        album_id = upsert_album(
            name,
            spotify_album_id,
            album_type,
            group_id,
            release_date,
            image_url,
            conn,
        )

        print(f"  Ingested: {name} (ID: {album_id})")

        ingest_tracks(
            token,
            spotify_album_id,
            album_id,
            group_id,
            conn,
        )

def ingest_tracks(token, spotify_album_id, album_id, group_id, conn):
    """Fetch tracks for an album and store them."""
    simple_tracks = get_album_tracks(token, spotify_album_id)

    track_ids = [track["id"] for track in simple_tracks]

    full_tracks = get_tracks(token, track_ids)

    for track in full_tracks:
        external_ids = track.get("external_ids") or {}
        isrc = external_ids.get("isrc")

        name = track["name"]
        spotify_track_id = track["id"]
        track_number = track["track_number"]
        disc_number = track["disc_number"]
        duration_ms = track["duration_ms"]
        
        track_id = upsert_track(
            name,
            spotify_track_id,
            track_number,
            disc_number,
            album_id,
            group_id,
            isrc,
            duration_ms,
            conn,
        )

        print(f"  Ingested: {name} (ID: {track_id})")

def main():
    query = " ".join(sys.argv[1:])

    if not query:
        print("Usage: python ingest.py <artist name>")
        return

    user_id = 1

    with get_connection() as conn:
        token = get_access_token(user_id, conn)

        artist = choose_artist(token, query)

        print(f"\nSelected: {artist['name']}")

        ingest_group(
            token,
            artist["id"],
            conn,
        )

if __name__ == "__main__":
    main()
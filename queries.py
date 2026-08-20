# queries.py
from db import fetch_all, execute

def upsert_user(spotify_user_id, display_name, image_url, conn):
    """Insert or update a Spotify user and return the internal user ID."""

    rows = fetch_all(
        """
        INSERT INTO users (spotify_user_id, display_name, image_url)
        VALUES (%s, %s, %s)
        ON CONFLICT (spotify_user_id) DO UPDATE SET
            display_name = EXCLUDED.display_name,
            image_url = EXCLUDED.image_url
        RETURNING id;
        """,
        (spotify_user_id, display_name, image_url),
        conn=conn,
    )
    return rows[0]["id"]

def upsert_spotify_token(user_id, access_token, refresh_token_encrypted, expires_at, conn):
    """Insert or update the Spotify tokens for a user."""

    execute(
        """
        INSERT INTO spotify_tokens (user_id, access_token, refresh_token_encrypted, expires_at)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            access_token = EXCLUDED.access_token,
            refresh_token_encrypted = EXCLUDED.refresh_token_encrypted,
            expires_at = EXCLUDED.expires_at
        """,
        (user_id, access_token, refresh_token_encrypted, expires_at),
        conn=conn,
    )

def upsert_group(name, spotify_artist_id, profile_image, conn):
    """Insert or update a group and return the internal group ID."""

    rows = fetch_all(
        """
        INSERT INTO groups (name, spotify_artist_id, profile_image)
        VALUES (%s, %s, %s)
        ON CONFLICT (spotify_artist_id) DO UPDATE SET
            name = EXCLUDED.name,
            profile_image = EXCLUDED.profile_image
        RETURNING id;
        """,
        (name, spotify_artist_id, profile_image),
        conn=conn,
    )
    return rows[0]["id"]

def upsert_album(name, spotify_album_id, album_type, group_id, release_date, image_url, conn):
    """Insert or update an album and return the internal album ID."""

    rows = fetch_all(
        """
        INSERT INTO albums (name, spotify_album_id, album_type, group_id, release_date, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (spotify_album_id) DO UPDATE SET
            name = EXCLUDED.name,
            album_type = EXCLUDED.album_type,
            group_id = EXCLUDED.group_id,
            release_date = EXCLUDED.release_date,
            image_url = EXCLUDED.image_url
        RETURNING id;
        """,
        (name, spotify_album_id, album_type, group_id, release_date, image_url),
        conn=conn,
    )
    return rows[0]["id"]

def upsert_track(name, spotify_track_id, track_number, disc_number, album_id, group_id, isrc, duration_ms, conn):
    """Insert or update a track and return the internal track ID."""

    rows = fetch_all(
        """
        INSERT INTO tracks (name, spotify_track_id, track_number, disc_number, album_id, group_id, isrc, duration_ms)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (spotify_track_id) DO UPDATE SET
            name = EXCLUDED.name,
            track_number = EXCLUDED.track_number,
            disc_number = EXCLUDED.disc_number,
            album_id = EXCLUDED.album_id,
            group_id = EXCLUDED.group_id,
            isrc = EXCLUDED.isrc,
            duration_ms = EXCLUDED.duration_ms
        RETURNING id;
        """,
        (name, spotify_track_id, track_number, disc_number, album_id, group_id, isrc, duration_ms),
        conn=conn,
    )
    return rows[0]["id"]

def upsert_top_track(user_id, spotify_track_id, position, time_range, conn):
    """Insert or update the user's top tracks."""

    execute(
        """
        INSERT INTO user_top_tracks (user_id, spotify_track_id, position, time_range, captured_on)
        VALUES (%s, %s, %s, %s, CURRENT_DATE)
        ON CONFLICT (user_id, time_range, captured_on, spotify_track_id) DO UPDATE SET
            position = EXCLUDED.position;
        """,
        (user_id, spotify_track_id, position, time_range),
        conn=conn,
    )

def upsert_saved_track(user_id, spotify_track_id, added_at, conn):
    """Insert or update a user's saved track."""

    execute(
        """
        INSERT INTO user_saved_tracks (
            user_id,
            spotify_track_id,
            added_at,
            captured_at
        )
        VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
        ON CONFLICT (user_id, spotify_track_id) DO UPDATE SET
            captured_at = CURRENT_TIMESTAMP;
        """,
        (user_id, spotify_track_id, added_at),
        conn=conn,
    )

def get_access_token(user_id, conn):
    """Return the stored Spotify access token for a user."""

    rows = fetch_all(
        """
        SELECT access_token
        FROM spotify_tokens
        WHERE user_id = %s
        """,
        (user_id,),
        conn=conn,
    )

    if not rows:
        raise ValueError("No Spotify token found for user")

    return rows[0]["access_token"]

def get_user(user_id, conn):
    """Return the user's Spotify profile information."""
    rows = fetch_all(
        """
        SELECT
            id,
            spotify_user_id,
            display_name,
            image_url
        FROM users
        WHERE id = %s;
        """,
        (user_id,),
        conn=conn,
    )

    return rows[0] if rows else None
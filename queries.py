# queries.py
from db import fetch_all, execute

def upsert_user(spotify_user_id, display_name, conn):
    """Insert or update a Spotify user and return the internal user ID."""

    rows = fetch_all(
        """
        INSERT INTO users (spotify_user_id, display_name)
        VALUES (%s, %s)
        ON CONFLICT (spotify_user_id) DO UPDATE SET
            display_name = EXCLUDED.display_name
        RETURNING id;
        """,
        (spotify_user_id, display_name),
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
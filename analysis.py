# analysis.py
from db import fetch_all, get_connection

def get_era_affinity(user_id, time_range, conn):
    """Calculate a user's affinity for each era based on their top tracks."""

    return fetch_all(
        """
        SELECT
            e.id AS era_id,
            e.name AS era,
            SUM(1.0 / utt.position) AS affinity_score
        FROM user_top_tracks utt
        JOIN tracks t
            ON utt.spotify_track_id = t.spotify_track_id
        JOIN albums a
            ON t.album_id = a.id
        JOIN eras e
            ON a.era_id = e.id
        WHERE utt.user_id = %s
          AND utt.time_range = %s
        GROUP BY e.id, e.name
        ORDER BY affinity_score DESC;
        """,
        (user_id, time_range),
        conn=conn,
    )

def get_top_track_for_era(user_id, era_id, time_range, conn):
    """Return the user's highest-ranked track from a given era."""

    rows = fetch_all(
        """
        SELECT
            t.name,
            t.spotify_track_id,
            utt.position
        FROM user_top_tracks utt
        JOIN tracks t
            ON utt.spotify_track_id = t.spotify_track_id
        JOIN albums a
            ON t.album_id = a.id
        JOIN eras e
            ON a.era_id = e.id
        WHERE utt.user_id = %s
          AND utt.time_range = %s
          AND e.id = %s
        ORDER BY utt.position
        LIMIT 1;
        """,
        (user_id, time_range, era_id),
        conn=conn,
    )

    return rows[0] if rows else None

def get_top_eras(user_id, time_range, conn, limit=5):
    """Return the user's top eras and their highest-ranked tracks."""

    eras = get_era_affinity(user_id, time_range, conn)

    results = []

    for era in eras[:limit]:
        top_track = get_top_track_for_era(
            user_id,
            era["era_id"],
            time_range,
            conn,
        )

        results.append({
            "era": era["era"],
            "affinity_score": era["affinity_score"],
            "top_track": top_track,
        })

    return results

def get_era_coverage(user_id, time_range, conn):
    """Calculate how much of each era's catalog the user has heard."""

    return fetch_all(
        """
        WITH heard AS (
            SELECT DISTINCT utt.spotify_track_id
            FROM user_top_tracks utt
            WHERE utt.user_id = %s
              AND utt.time_range = %s

            UNION

            SELECT DISTINCT ust.spotify_track_id
            FROM user_saved_tracks ust
            WHERE ust.user_id = %s
        ),

        era_totals AS (
            SELECT
                e.id AS era_id,
                e.name AS era,
                COUNT(DISTINCT COALESCE(t.isrc, t.spotify_track_id)) AS total_tracks
            FROM eras e
            JOIN albums a
                ON a.era_id = e.id
            JOIN tracks t
                ON t.album_id = a.id
            GROUP BY e.id, e.name
        ),

        era_heard AS (
            SELECT
                e.id AS era_id,
                COUNT(DISTINCT COALESCE(t.isrc, t.spotify_track_id)) AS heard_tracks
            FROM heard h
            JOIN tracks t
                ON t.spotify_track_id = h.spotify_track_id
            JOIN albums a
                ON t.album_id = a.id
            JOIN eras e
                ON a.era_id = e.id
            GROUP BY e.id
        )

        SELECT
            et.era_id,
            et.era,
            COALESCE(eh.heard_tracks, 0) AS heard_tracks,
            et.total_tracks,
            COALESCE(eh.heard_tracks, 0)::numeric / et.total_tracks
                AS coverage
        FROM era_totals et
        LEFT JOIN era_heard eh
            ON eh.era_id = et.era_id
        ORDER BY coverage DESC;
        """,
        (user_id, time_range, user_id),
        conn=conn,
    )

if __name__ == "__main__":
    with get_connection() as conn:
        results = get_era_coverage(
            1,
            "long_term",
            conn,
        )

        for row in results:
            print(row)
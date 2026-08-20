# analysis.py
from db import fetch_all, get_connection

def get_era_affinity(user_id, time_range, conn):
    """Calculate a user's affinity for each era based on their top tracks."""

    return fetch_all(
        """
        SELECT
            e.id AS era_id,
            e.name AS era,
            e.group_id,
            g.name AS group_name,
            g.profile_image,
            SUM(1.0 / utt.position) AS affinity_score
        FROM user_top_tracks utt
        JOIN tracks t
            ON utt.spotify_track_id = t.spotify_track_id
        JOIN albums a
            ON t.album_id = a.id
        JOIN eras e
            ON a.era_id = e.id
        JOIN groups g
            ON e.group_id = g.id
        WHERE utt.user_id = %s
          AND utt.time_range = %s
        GROUP BY e.id, e.name, g.id, g.name, g.profile_image
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

def get_top_track_for_group(user_id, group_id, time_range, conn):
    """Return the user's highest-ranked track from a group."""

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
          AND e.group_id = %s
        ORDER BY utt.position
        LIMIT 1;
        """,
        (user_id, time_range, group_id),
        conn=conn,
    )

    return rows[0] if rows else None

def get_group_analysis(user_id, time_range, conn):
    """Rank groups by the combined affinity of their eras."""

    era_affinity = get_era_affinity(user_id, time_range, conn)

    groups = {}

    for era in era_affinity:
        group_id = era["group_id"]

        if group_id not in groups:
            groups[group_id] = {
                "group_id": group_id,
                "group_name": era["group_name"],
                "profile_image": era["profile_image"],
                "score": 0,
                "eras": [],
            }

        groups[group_id]["score"] += era["affinity_score"]
        groups[group_id]["eras"].append(era)

    results = list(groups.values())

    results.sort(
        key=lambda group: group["score"],
        reverse=True,
    )

    for group in results:
        max_score = group["eras"][0]["affinity_score"] if group["eras"] else 1

        for era in group["eras"]:
            era["bar_width"] = (
                era["affinity_score"] / max_score * 100
                if max_score
                else 0
            )

    return results

def get_user_analysis(user_id, conn):
    """Build the listening analysis for the logged-in user."""

    analysis = {}

    for time_range in ("short_term", "medium_term", "long_term"):

        groups = get_group_analysis(
            user_id,
            time_range,
            conn,
        )

        for group in groups:
            group["top_era"] = (
                group["eras"][0]
                if group["eras"]
                else None
            )

            group["top_track"] = get_top_track_for_group(
                user_id,
                group["group_id"],
                time_range,
                conn,
            )

        analysis[time_range] = {
            "groups": groups,
            "top_groups": groups[:5],
            "top_group": groups[0] if groups else None,
        }

    return analysis
        
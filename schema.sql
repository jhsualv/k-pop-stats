-- Catalog tables are rebuilt from Spotify while user tables persist
DROP TABLE IF EXISTS tracks;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS eras;
DROP TABLE IF EXISTS groups;

CREATE TABLE groups (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
spotify_artist_id TEXT UNIQUE NOT NULL,
profile_image TEXT
);

CREATE TABLE eras (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
group_id INTEGER NOT NULL REFERENCES groups(id),
month INTEGER NOT NULL CHECK (month between 1 AND 12),
year INTEGER NOT NULL,
UNIQUE (group_id, name)
);

CREATE TABLE albums (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
spotify_album_id TEXT UNIQUE NOT NULL,
album_type TEXT,
era_id INTEGER REFERENCES eras(id),
group_id INTEGER NOT NULL REFERENCES groups(id),
release_date DATE
);

CREATE TABLE tracks (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
spotify_track_id TEXT UNIQUE NOT NULL,
popularity INTEGER,
popularity_captured_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
track_number INTEGER,
disc_number INTEGER,
album_id INTEGER NOT NULL REFERENCES albums(id),
group_id INTEGER NOT NULL REFERENCES groups(id),
isrc TEXT,
duration_ms INTEGER
);

CREATE TABLE users (
id SERIAL PRIMARY KEY,
spotify_user_id TEXT UNIQUE NOT NULL,
display_name TEXT,
created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_top_tracks (
user_id INTEGER NOT NULL REFERENCES users(id),
spotify_track_id TEXT NOT NULL,
position INTEGER NOT NULL,
time_range TEXT CHECK (time_range IN ('short_term', 'medium_term', 'long_term')),
captured_on DATE NOT NULL,
PRIMARY KEY (user_id, time_range, captured_on, spotify_track_id)
);

CREATE TABLE user_saved_tracks (
user_id INTEGER NOT NULL REFERENCES users(id),
spotify_track_id TEXT NOT NULL,
captured_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
added_at TIMESTAMPTZ,
PRIMARY KEY (user_id, spotify_track_id)
);

CREATE TABLE spotify_tokens (
user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
access_token TEXT,
refresh_token_encrypted TEXT NOT NULL, -- TODO: implement encryption for stored refresh token
expires_at TIMESTAMPTZ NOT NULL,
created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- musicbrainz_setup.sql
-- Script to set up the MusicBrainz database schema

-- Create the artists table
CREATE TABLE IF NOT EXISTS artists (
    artist_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

-- Create the albums table
CREATE TABLE IF NOT EXISTS albums (
    album_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    artist_id INTEGER NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

-- Create the releases table
CREATE TABLE IF NOT EXISTS releases (
    mbid TEXT PRIMARY KEY,
    album_id INTEGER NOT NULL,
    release_data JSONB NOT NULL,
    FOREIGN KEY (album_id) REFERENCES albums(album_id)
);

-- Create indexes for JSONB data and full-text search
CREATE INDEX IF NOT EXISTS idx_release_data ON releases USING GIN (release_data);
CREATE INDEX IF NOT EXISTS idx_artist_name ON artists USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_album_title ON albums USING GIN (title gin_trgm_ops);

-- Optional: Insert some initial data (examples)
INSERT INTO artists (name) VALUES ('Artist 1'), ('Artist 2');
INSERT INTO albums (title, artist_id) VALUES ('Album 1', 1), ('Album 2', 2);

-- End of script

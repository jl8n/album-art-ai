import psycopg2
from psycopg2 import sql
import json


def insert_data(mbid: str, data: str, album: str, artist: str) -> None:
    conn = psycopg2.connect(
        dbname="musicbrainz",
        user="postgres",
        password="example",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Upsert artist
    cur.execute(
        """
        INSERT INTO artists (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING;
        """,
        (artist,)
    )

    # Upsert album
    cur.execute(
        """
        INSERT INTO albums (title, artist_id)
        SELECT %s, artist_id FROM artists WHERE name = %s
        ON CONFLICT (title, artist_id) DO NOTHING;
        """,
        (album, artist)
    )

    # Insert release
    cur.execute(
        """
        INSERT INTO releases (mbid, album_id, release_data)
        SELECT %s, album_id, %s FROM albums
        INNER JOIN artists ON albums.artist_id = artists.artist_id
        WHERE albums.title = %s AND artists.name = %s
        ON CONFLICT (mbid) DO NOTHING;
        """,
        (mbid, data, album, artist)
    )

    # Commit changes to the database
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()


def get_data(mbid: str) -> str:
    # Define your connection parameters
    conn = psycopg2.connect(
        dbname="musicbrainz_results",
        user="postgres",
        password="example",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    select_statement = sql.SQL(
        "SELECT * FROM releases WHERE mbid = %s"
    )

    # Execute the SQL command
    cur.execute(select_statement, (mbid,))

    # Fetch the result
    result = cur.fetchone()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Convert the result to JSON and return it
    return json.dumps(result)

import psycopg2
from psycopg2 import sql
import json


def insert_data(mbid: str, data: str, album: str, artist: str) -> None:
    conn = psycopg2.connect(
        dbname="musicbrainz_results",
        user="postgres",
        password="example",
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    insert_statement = sql.SQL(
        """
        INSERT INTO releases (mbid, album, artist, data) 
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (mbid) DO NOTHING
        """
    )

    # Execute SQL command
    cur.execute(insert_statement, (mbid, album, artist, data))

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

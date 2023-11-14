from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
import requests
from urllib.parse import urlencode
import os

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


def getCandidateMBIDs(artist: str, album: str) -> list[str]:
    query = f"artist:{artist} AND release:{album}"
    params = urlencode({"query": query, "fmt": "json", "limit": 5})

    api_url = f"http://musicbrainz.org/ws/2/release/?{params}"
    print(api_url)
    response = requests.get(api_url)
    data = response.json()

    # Extract the MBIDs from the releases
    mbids = [release["id"] for release in data["releases"]]
    return mbids


def downloadImage(image_url: str, mbid: str) -> bool:
    # Download image if it doesn't already exist
    existing_path = f"../static/album-art/{mbid}.jpg"
    if not os.path.exists(existing_path):
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()  # Ensure we got a valid response
        except requests.exceptions.RequestException:
            return False
    else:
        print(f"EXISTS {mbid}")
        return True

    # Save image to filesystem
    image_path = os.path.join("../static/album-art", f"{mbid}.jpg")
    with open(image_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    return True


def downloadAlbumArt(mbid: str):
    api_url = f"https://coverartarchive.org/release/{mbid}"
    response = requests.get(api_url)

    # Check if the response is not empty and is in JSON format
    if response.text.strip() and response.headers["Content-Type"] == "application/json":
        data = response.json()
    else:
        print(f"No image found for {mbid}\n")
        return False

    # Create the album-art directory if it doesn't exist
    if not os.path.exists("../static/album-art"):
        os.makedirs("../static/album-art")

    # Download image from the URL in the coverartarchive.org response
    image_url = data["images"][0]["image"]
    downloadImage(image_url, mbid)


@app.route("/")
def search_for_album():
    """
    Searches ListenBrainz for a artist+album combo supplied by the user.
    Retrieves an MBID for each search result.
    Searches CoverArtArchive for album art for each MBID.
    Returns a list of MBIDs with existing album art to the client.
    """
    artist = request.args.get("artist", default="", type=str)
    album = request.args.get("album", default="", type=str)

    print(f"artist: {artist}\nalbum: {album}")
    mbids = getCandidateMBIDs(artist, album)

    for mbid in mbids:
        downloadAlbumArt(mbid)

    files = os.listdir("../static/album-art/")
    existing_files = [f for f in files if f.replace(".jpg", "") in mbids]
    return jsonify(existing_files)


@app.route("/album-art/<path:filename>")
@cross_origin()
def serve_file(filename):
    """Statically hosts album art downloaded from CoverArtArchive"""
    return send_from_directory("../static/album-art/", filename)


if __name__ == "__main__":
    app.run(debug=True)

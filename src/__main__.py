import api
from utils import load_folder, create_playlist


def run():
    # load and parse files
    path = input("Where should I search for music files? ")
    musics = list(load_folder(path))

    # Search and get Spotify ID from files' metadata
    spotipy = api.API()
    for music in musics:
        spotipy.search(music)

    # Get music features
    spotipy.feature_bulk(musics)
    create_playlist(musics, "lol.m3u")


if __name__ == "__main__":  # well, it's obvious
    run()

import logging
import os
import pickle
import api

from typing import List

from objects.song import Song
from utils import load_folder, create_playlist, list_files

PICKLE = "../dump.pickle"


def load(path: str = None) -> List[Song]:
    logging.info("Creating dataset")

    # Load and parse files
    if path is None:
        path = input("Where should I search for music files? ")
    musics = list(load_folder(path))
    logging.info("Completed files parsing")

    # Search and get Spotify ID from files' metadata
    spotipy = api.API()
    for music in musics:
        try:
            spotipy.search(music)
        except IndexError:
            logging.warning(f"{music['title']} - {music['artist']} not found. Skipping {music['path']}")
            musics.remove(music)
            continue
    logging.info("Completed spotify ids retrieving")

    # Get music features
    spotipy.feature_bulk(musics)
    logging.info("Completed spotify features retrieving")

    # Save data
    with open(PICKLE, "wb") as data:
        pickle.dump(musics, data)

    # Return data
    return musics


def load_with_pickle() -> List[Song]:
    with open(PICKLE, "rb") as data:
        logging.info("Loading already serialized dataset")
        songs = pickle.load(data)

    # List paths
    path = input("Where should I search for music files? ")
    files = list(load_folder(path))

    logging.info("Checking data")

    if len(files) != len(songs):
        logging.warning("New files found. Regenerating data set")

    return load(path)


def run():
    if os.path.isfile(PICKLE):
        songs = load_with_pickle()
    else:
        songs = load()

    logging.info("Creating playlist")
    create_playlist(songs, "../lol.m3u")

    logging.info("Complete")


if __name__ == "__main__":  # well, it's obvious
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    run()

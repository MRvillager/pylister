import logging
import os
import pickle
import api

from typing import List

from objects.song import Song
from utils import load_folder, create_playlist

PICKLE = "../dump.pickle"


def load() -> List[Song]:
    # Load and parse files
    path = input("Where should I search for music files? ")
    musics = list(load_folder(path))

    # Search and get Spotify ID from files' metadata
    spotipy = api.API()
    for music in musics:
        spotipy.search(music)

    # Get music features
    spotipy.feature_bulk(musics)

    # Save data
    with open(PICKLE, "wb") as data:
        pickle.dump(musics, data)

    # Return data
    return musics


if __name__ == "__main__":  # well, it's obvious
    if os.path.isfile(PICKLE):
        with open(PICKLE, "rb") as data:
            logging.info("Loading already serialized dataset")
            songs = pickle.load(data)
    else:
        logging.info("Creating dataset")
        songs = load()

    logging.info("Creating playlist")
    create_playlist(songs, "../lol.m3u")

    logging.info("Complete")

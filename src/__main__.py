import logging
import os
import pickle
from typing import List

import api
from clustering import cluster
from objects.song import Song
from utils import load_folder, create_playlist

PICKLE = "../dump.pickle"


def load(path: str = None) -> List[Song]:
    """
    Given a dir, creates a list of Song objects using found music files
    Args:
        path: the directory to search in

    Returns:
        A list of Song objects
    """
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
            spotipy.search(music, True)
        except IndexError:
            try:
                spotipy.search(music)
            except IndexError:
                logging.warning(f"{music['title']} - {music['artist']} not found. Skipping {music['path']}")
                musics.remove(music)
                continue
        if music["spotify_id"] is None:
            logging.error("error")
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
    """
    Load a pickle file
    Returns:
        A list of Song objects
    """
    with open(PICKLE, "rb") as data:
        logging.info("Loading already serialized dataset")
        songs = pickle.load(data, encoding="utf-8")

    return songs


def run():
    """
    Main function of the program
    Returns:
        None
    """
    if os.path.isfile(PICKLE):
        songs = load_with_pickle()
    else:
        songs = load()

    logging.info("Clustering")
    clusters = cluster(songs)

    logging.info("Creating playlist")
    create_playlist(clusters, "../test/lol.m3u")

    logging.info("Complete")


if __name__ == "__main__":  # well, it's obvious
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    run()

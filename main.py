import logging
import pickle
import os

from typing import List

# PyLister
from pylister import api
from pylister.clustering import cluster
from pylister.objects.song import Song
from pylister.utils import load_folder, create_playlist


PICKLE = "data.pickle"
FILENAME = "playlist.m3u"


def load(path: str = None) -> List[Song]:
    """
    Given a dir, creates a list of Song objects using found music files
    Args:
        path: the directory to search in

    Returns:
        A list of Song objects
    """
    logging.info("Creating dataset")

    # Get directory from user
    if path is None:
        path = input("Where should I search for music files? ")
    # Load and parse files
    musics = list(load_folder(path))
    logging.info("Completed files parsing")

    # Initialize API
    spotipy = api.API()
    # Search and get Spotify ID from files' metadata
    for music in musics:
        try:
            spotipy.search(music, True)  # Search using isrc
        except IndexError:  # Not found
            try:
                spotipy.search(music)  # Search using artist, title and year
            except IndexError:  # Not found, again
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
    cluster_n = int(input("How many playlists to create: "))
    clusters = cluster(songs, cluster_n)

    logging.info("Creating playlist")
    playlist_dir = input("choose the directory in which to put the playlists: ")
    create_playlist(clusters, os.path.join(playlist_dir, FILENAME))

    logging.info("Complete")


if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    run()

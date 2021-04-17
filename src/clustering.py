import logging
from typing import List

import numpy as np
from sklearn.cluster import KMeans

from objects.song import Song

# How many playlist to create
# TODO: let it choose using stdin
CLUSTER_N = 7


def cluster(raw_dataset: List[Song]) -> list:
    """
    Given a list of songs, cluster them using KMeans algorithm
    Args:
        raw_dataset: a list of Song objects

    Returns:
        a clustered list
    """
    dataset = prepare_data(raw_dataset)
    kmeans = KMeans(n_clusters=CLUSTER_N, random_state=0, n_init=20, tol=1e-06).fit(dataset)

    labels = kmeans.labels_
    out = [[] * CLUSTER_N]
    for i in range(len(raw_dataset)):
        j = labels[i]
        out[j].append(raw_dataset[i])

    return out


def prepare_data(songs: List[Song]) -> np.array:
    """
    Transform features of songs into a numpy array
    Args:
        songs: a list of Song objects

    Returns:
        A numpy array
    """
    raw_dataset = []
    for song in songs:
        try:
            raw_dataset.append(list(song["features"].items()))
        except AttributeError:
            logging.error(f"{song['title']} - {song['artist']} doesn't have a features object")

    return np.array(raw_dataset)

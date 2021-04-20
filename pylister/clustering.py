import logging
from typing import List

import numpy as np
from sklearn.cluster import KMeans

from objects.song import Song


def cluster(raw_dataset: List[Song], cluster_n: int = 5) -> list:
    """
    Given a list of songs, cluster them using KMeans algorithm
    Args:
        raw_dataset: a list of Song objects

    Returns:
        a clustered list
    """
    raw_dataset, dataset = prepare_data(raw_dataset)
    kmeans = KMeans(n_clusters=CLUSTER_N, random_state=0, n_init=20, tol=1e-06).fit(dataset)

    labels = kmeans.labels_

    # Create return list
    out = []
    for _ in range(CLUSTER_N):
        out.append([])

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
    fixed_songs = []
    for song in songs:
        if song["features"] is None:
            continue
        else:
            raw_dataset.append(list(song["features"].items()))
            fixed_songs.append(song)

    return fixed_songs, np.array([np.array(dataset) for dataset in raw_dataset])

from typing import List

import numpy as np
from sklearn.cluster import KMeans

from pylister.song import Song


def cluster(raw_dataset: List[Song], cluster_n: int = 4, mode: list = None) -> list:
    """
    Given a list of songs, cluster them using KMeans algorithm
    Args:
        raw_dataset: a list of Song objects
        cluster_n: how many clusters create
        mode: the feature(s) to use for clustering

    Returns:
        a clustered list
    """
    raw_dataset, dataset = prepare_data(raw_dataset, mode)
    kmeans = KMeans(n_clusters=cluster_n, random_state=0, n_init=20, tol=1e-06)
    kmeans.fit(dataset)

    # Create return list
    out = []
    for _ in range(cluster_n):
        out.append([])

    labels = kmeans.labels_
    for i, music in enumerate(raw_dataset):
        j = labels[i]
        out[j].append(music)

    return out


def prepare_data(songs: List[Song], mode: list) -> np.array:
    """
    Transform features of songs into a numpy array
    Args:
        songs: a list of Song objects
        mode: the feature(s) to use for creating the dataset

    Returns:
        A numpy array
    """
    raw_dataset = []
    fixed_songs = []
    for song in songs:
        if song["features"] is None:
            continue
        else:
            if mode is None:
                raw_dataset.append(list(song["features"].items()))
            else:
                raw_dataset.append(list(song["features"].group(mode)))

            fixed_songs.append(song)

    return fixed_songs, np.array([np.array(dataset) for dataset in raw_dataset])

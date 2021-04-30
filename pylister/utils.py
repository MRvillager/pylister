import logging
import os
import re
from typing import List

import mutagen

from pylister.song import Song

FILE_FORMATS = [".mp3", ".flac", ".ogg"]


def load_folder(track_dir: str) -> list:
    """
    Load and parse all the files in a folder
    Args:
        track_dir: the directory to search in

    Returns:
        a list containing the Music Objects
    """
    files = list_files(track_dir)
    for file in files:
        yield load_file(file)


def list_files(track_dir: str) -> list:
    """
    Given a dir, list all the files and subdirs
    Args:
        track_dir: the directory to search in

    Returns:
        None
    """
    for path, subdirs, files in os.walk(track_dir):
        for name in files:
            if os.path.splitext(name)[1] in FILE_FORMATS:
                yield os.path.join(path, name)


def load_files(files: List[str]) -> list:
    """
    Load and parse all the files
    Args:
        files: a list of files to parse

    Returns:
        a list containing the Music Objects
    """
    for file in files:
        yield load_file(file)


def load_file(track_path: str) -> Song:
    """
    Load and parse the given file
    Args:
        track_path: the path of the music file

    Returns:
        A Music Object created from the file
    """
    path = os.path.abspath(track_path)
    file = mutagen.File(path)

    title = str(file["title"][0])

    album = str(file["album"][0])

    try:
        isrc = str(file["isrc"][0])
    except KeyError:
        logging.debug(f"isrc not found in {path}")
        isrc = None

    try:
        artist = ", ".join(file["artist"])
    except KeyError:
        artist = str(file["albumartist"][0])

    try:
        # Extract year from year :)
        year = int(file["year"][0])
    except KeyError:
        try:
            # Extract year from date string
            rx_str = "(\\d\\d\\d\\d)"
            date = file["date"][0]
            year = int(re.search(rx_str, date).group(0))
        except KeyError:
            # Extract year from copyright string
            rx_str = "(\\d\\d\\d\\d)"
            cp = file["copyright"][0]
            year = int(re.search(rx_str, cp).group(0))

    return Song(title=title, artist=artist, album=album, year=year, path=path, isrc=isrc)


def create_playlist(clusters: List[List[Song]], filename: str) -> None:
    """
    Create playlists from the clusters list
    Args:
        clusters: A list of list of song
        filename: the base filename to use to save the playlists

    Returns:
        None
    """
    # split filename and extension
    filename, file_extension = os.path.splitext(filename)
    for i, cluster in enumerate(clusters):
        file = f"{filename}.{i}{file_extension}"  # test.4.m3u
        playlist = open(file, "w", encoding="utf-8")

        for music in cluster:
            playlist.write(f"{music['path']}\n")

        playlist.close()

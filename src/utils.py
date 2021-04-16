import os
import re
import mutagen

from typing import List
from objects.song import Song

FILE_FORMATS = [".mp3", ".flac", ".ogg"]


def load_folder(track_dir: str) -> list:
    """
    Load and parse all the files in a folder
    Args:
        track_dir: the folder containing the music files

    Returns:
        a list containing the Music Objects
    """
    files = list_files(track_dir)
    for file in files:
        yield load_file(file)


def list_files(track_dir: str) -> list:
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
    file = mutagen.File(track_path)

    title = str(file["title"][0])

    album = str(file["album"][0])

    try:
        artist = ", ".join(file["artist"])
    except KeyError:
        try:
            artist = str(file["albumartist"][0])
        except KeyError:
            artist = str(file["artist"][0])

    try:
        year = int(file["year"][0])
    except KeyError:
        try:
            date = file["date"][0].split("-")
            year = 0
            for elem in date:
                if len(elem) == 4:
                    year = int(elem)
        except KeyError:
            rx_str = "(\\d\\d\\d\\d)"
            cp = file["copyright"][0]
            year = int(re.search(rx_str, cp).group(0))

    return Song(title, artist, album, year, os.path.abspath(track_path))


def create_playlist(musics: list, filename: str):
    playlist = open(filename, "w")

    for music in musics:
        playlist.write(f"{music['path']}\n")

    playlist.close()

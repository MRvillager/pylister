import os

import mutagen

from objects.song import Song


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
            yield os.path.join(path, name)


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
    artist = str(file["albumartist"][0])
    year = int(file["year"][0])

    return Song(title, artist, album, year, os.path.abspath(track_path))


def create_playlist(musics: list, filename: str):
    playlist = open(filename, "w")

    for music in musics:
        playlist.write(f"{music['path']}\n")

    playlist.close()

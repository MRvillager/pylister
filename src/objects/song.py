import logging
from typing import Union

from .analysis import Analysis
from .features import Feature


class Song:
    _title = None
    _artist = None
    _album = None
    _year = None

    _path = None
    _spotify_id = None

    _features = None
    _analysis = None

    _keys = [
        "title",
        "artist",
        "album",
        "year",
        "path",
        "spotify_id",
        "features",
        "analysis",
    ]

    def __init__(self, title: str, artist: str, album: str, year: Union[str, int], path: str,
                 spotify_id: str = None, features: Feature = None, analysis: Analysis = None):

        self._title = title
        self._artist = artist
        self._album = album
        self._year = year

        self._path = path
        self._spotify_id = spotify_id

        self._features = features
        self._analysis = analysis

    def __doc__(self):
        return "This object is used to store the metadata of music files and their path on the pc and on spotify"

    def __name__(self):
        return self._title

    def __len__(self):
        """
        Use to get the number of the keys used

        Returns:
            the length of the _key list
        """
        return len(self._keys)

    def __missing__(self, key: str):
        """
        Raises error when the given key is not found

        Args:
            key: Represent the not found key

        Returns:
            None

        Raises:
            KeyError: the key was not found or it's not considered
        """
        logging.warning(f"{key} not found in {self._path} class")
        raise KeyError(f"{key} not found in {self._path} class")

    def __getitem__(self, key: str) -> Union[str, int, None, dict]:
        """
        Returns an item given the key

        Args:
            key: it's a string representing the value to return

        Returns:
            the value requested
        """
        if key not in self._keys:
            return self.__missing__(key)

        return self.__dict__[f"_{key}"]

    def __setitem__(self, key, value: str) -> None:
        """
        Set a value to the given key

        Args:
            key: it's a string representing the value to modify
            value: the value to set to the key

        Returns:
            None
        """
        if key not in self._keys:
            return self.__missing__(key)

        self.__dict__[f"_{key}"] = value

    def __iter__(self):
        return MusicIterator(music=self)

    def keys(self) -> list:
        """
        Use to get the available keys

        Returns:
            The list containing the keys
        """
        return self._keys

    def items(self):
        """
        Get a list of all the items available

        Returns:
            The list containing the items
        """
        for key in self._keys:
            yield self.__dict__[f"_{key}"]

    def set_spotipy_id(self, data: dict) -> None:
        """
        Get and set the spotify id from a json object from spotiapi
        Args:
            data: a json object from spotiapi representing the song

        Returns:
            None
        """
        self._spotify_id = data["id"]

    def set_features(self, data: dict) -> None:
        """
        Get and set the spotify id from a json object from spotiapi
        Args:
            data: a json object from spotiapi representing the song

        Returns:
            None
        """
        del data["type"]
        del data["id"]
        del data["uri"]
        del data["track_href"]
        del data["analysis_url"]
        self._features = Feature(**data)

    def set_analysis(self, data: dict) -> None:
        raise NotImplementedError()


class MusicIterator:
    """
    Iterator class

    Args:
        music: it's the Music object to iter
    """

    def __init__(self, music: Song):
        self._music = music
        self._keys = self._music.keys
        self._keys_len = len(self._keys)
        self._index = 0

    def __next__(self) -> Union[str, Feature, None, dict]:
        """
        Used to iter over the Music Object

        Returns:
            the next key's value

        Raises:
            StopIteration: when reaches the end
        """
        if self._index < self._keys_len:
            result = self._music[self._keys[self._index]]
            self._index += 1
            return result
        else:
            # End of Iteration
            raise StopIteration

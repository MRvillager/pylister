import logging
from typing import Union


class Feature:
    _danceability = None
    _energy = None
    _key = None
    _loudness = None
    _mode = None
    _speechiness = None
    _acousticness = None
    _instrumentalness = None
    _liveness = None
    _valence = None
    _tempo = None

    _duration_ms = None
    _time_signature = None

    _keys = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness',
             'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    def __init__(self, danceability: float, energy: float, key: int, loudness: float, mode: int, speechiness: float,
                 acousticness: float, instrumentalness: float, liveness: float, valence: float, tempo: float,
                 duration_ms: float,
                 time_signature: int):
        self.danceability = danceability
        self.energy = energy
        self.key = key
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.acousticness = acousticness
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.tempo = tempo

        self.duration_ms = duration_ms
        self.time_signature = time_signature

    def __len__(self) -> int:
        """
        Use to get the number of the keys used

        Returns:
            the length of the _key list
        """
        return len(self._keys)

    def __missing__(self, key: str) -> None:
        """
        Raises error when the given key is not found

        Args:
            key: Represent the not found key

        Returns:
            None

        Raises:
            KeyError: the key was not found or it's not considered
        """
        logging.warning(f"{key} not found")
        raise KeyError(f"{key} not found")

    def __getitem__(self, key: str) -> int:
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
        return FeaturesIterator(self)

    @property
    def keys(self) -> list:
        """
        Use to get the available keys

        Returns:
            The list containing the keys
        """
        return self._keys


class FeaturesIterator:
    def __init__(self, feature: Feature):
        self._features = feature
        self._keys = self._features.keys
        self._keys_len = len(self._keys)
        self._index = 0

    def __next__(self) -> Union[float, int]:
        """
        Used to iter over the Features Object

        Returns:
            the next key's value

        Raises:
            StopIteration: when reaches the end
        """
        if self._index < self._keys_len:
            result = self._features[self._keys[self._index]]
            self._index += 1
            return result
        else:
            # End of Iteration
            raise StopIteration

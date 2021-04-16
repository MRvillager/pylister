import base64
import logging
import os
from typing import List

from requests import Session, post

from objects.song import Song


class API:
    _ID = None  # First line
    _SECRET = None  # Second line
    _TOKEN_URL = "https://accounts.spotify.com/api/token"
    _SEARCH_URL = "https://api.spotify.com/v1/search"
    _FEATURES_URL = "https://api.spotify.com/v1/audio-features/"
    _ANALYSIS_URL = "https://api.spotify.com/v1/audio-analysis/"

    _MAX_IDS = 100

    def __init__(self):
        self.session = Session()

        self.key_parse()
        self.auth()

    def __list_split(self, split: list, n: int) -> list:
        """
        Split the given list every nth element
        Args:
            split: the list to split
            n: the size of splitted lists

        Returns:
            The lists splitted
        """
        for i in range(0, len(split), n):
            # Create an index range for l of n items:
            yield split[i:i + n]

    def __ids_assembler(self, tracks: List[Song]) -> str:
        """
        Given a list of Song Objects, extract spotify ids and assemble them in a string
        Args:
            tracks: a list of Song Objects

        Returns:
            A string with every element of the list separated with a comma
        """
        out = ""
        for track in tracks:
            out += f"{track['spotify_id']},"
        return out[:-1]

    def key_parse(self) -> None:
        """
        Load the client id and the client secret from the .key file
        Returns:
            None
        """
        keyname = ".key"

        logging.debug(f"Parsing {keyname}")
        with open(os.path.join("../", keyname), "r") as keyfile:
            lines = keyfile.readlines()

            # File Sanitizing
            if len(lines) != 2:
                logging.warning(f"{keyname} should have 2 lines")

            for _, line in zip(range(2), lines):
                if len(line) != 33:  # 32 + \n
                    logging.critical("Client id and client secret must have 32 chars")
                    raise ValueError("Client id and client secret must have 32 chars")

            self._ID = lines[0].replace("\n", "")
            self._SECRET = lines[1].replace("\n", "")

    def auth(self) -> None:
        """
        Get an oauth token from the Spotify Web API
        Returns:
            None
        """
        auth_str = bytes(f"{self._ID}:{self._SECRET}", 'utf-8')
        auth_b64 = base64.b64encode(auth_str).decode('utf-8')
        headers = {
            "Authorization": f"Basic {auth_b64}"
        }
        body = {"grant_type": "client_credentials"}

        response = post(url=self._TOKEN_URL, headers=headers, data=body)
        data = response.json()

        token_header = {"Authorization": f"Bearer {data['access_token']}"}

        self.session.headers = token_header

    def search(self, track: Song) -> None:
        """
        Search a song using the Spotify Web API
        Args:
            track: the Song Object representing the track to search

        Returns:
            None
        """
        query = f"{track['title']}%20artist:{track['artist']}%20year:{track['year']}&type=track"
        url = f"{self._SEARCH_URL}?q={query}"

        response = self.session.get(url=url)
        if response.status_code != 200:
            logging.warning(f"Search request failed. Status = {response.status_code} - Url = {url} - Response = "
                            f"{response.content}")
            raise ValueError(f"Search request failed.")

        data = response.json()["tracks"]["items"][0]
        track.set_spotipy_id(data)

    def feature_bulk(self, tracks: List[Song]) -> None:
        """
        Get the song features for a list of Song Objects
        Args:
            tracks: a list of Song Objects

        Returns:
            None
        """
        tracks_chunks = self.__list_split(tracks, self._MAX_IDS)

        for chunk in tracks_chunks:
            self.features(chunk)

    def features(self, tracks: List[Song]) -> None:
        """
        Get the song features for a list of ids with a max size of 100 tracks
        Args:
            tracks: a list of Song Objects with at maximum 100 elements

        Returns:
            None
        """
        path = self.__ids_assembler(tracks)
        url = f"{self._FEATURES_URL}?ids={path}"

        response = self.session.get(url=url)
        if response.status_code != 200:
            logging.warning(f"Features request failed. Status = {response.status_code} - Url = {url} - Response = "
                            f"{response.content}")
            raise ValueError(f"Feature request failed.")

        data = response.json()["audio_features"]

        for track in tracks:  # This is solution it's extremely slow. TODO: found an alternative
            for feature in data:
                try:
                    if feature["id"] == track["spotify_id"]:
                        track.set_features(data.pop(data.index(feature)))
                        break
                except TypeError:
                    pass
                    # logging.warning(f"Cannot check {feature} when looping on {track['title']} - {track['artist']}"
                    #                f"Maybe it's already claimed")

    def analysis(self, track: Song) -> None:
        """
        Get the audio analysis for a track
        Args:
            track: the Song Object representing the track to analyse

        Returns:
            None
        """
        url = f"{self._ANALYSIS_URL}{track['spotify_id']}"

        response = self.session.get(url=url)
        if response.status_code != 200:
            logging.warning(f"Analysis request failed. Status = {response.status_code} - Url = {url} - Response = "
                            f"{response.content}")
            raise ValueError(f"Analysis request failed.")

        data = response.json()["track"]

        track["analysis"] = data  # TODO: Analysis object

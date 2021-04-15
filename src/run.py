from utils import loader, playlist
import api


def run():
    # load and parse files
    path = input("Where should I search for music files? ")
    musics = list(loader.load_folder(path))

    # Search and get Spotify ID from files' metadata
    spotipy = api.API()
    for music in musics:
        spotipy.search(music)

    # Get music features
    spotipy.feature_bulk(musics)
    playlist.create_playlist(musics, "lol.m3u")


if __name__ == "__main__":
    run()

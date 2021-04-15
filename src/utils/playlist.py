def create_playlist(musics: list, filename: str):
    playlist = open(filename, "w")

    for music in musics:
        playlist.write(f"{music['path']}\n")

    playlist.close()

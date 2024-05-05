class MusicNotFoundError(Exception):
    def __init__(self, spotify_track_id: str):
        self.spotify_track_id = spotify_track_id
        super().__init__(f"Music {self.spotify_track_id} not found")

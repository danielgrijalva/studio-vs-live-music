import decouple
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self):
        self.client_id = decouple.config("CLIENT_ID")
        self.client_secret = decouple.config("CLIENT_SECRET")
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=self.client_id, client_secret=self.client_secret
            )
        )

    def get_analyzed_tracklist(self, album_url: str) -> list:
        """
        Get the audio features for each track in an album and return the album
        tracklist as a list of dictionaries. Example:
            [
                {
                    'artist': "You'll Never Get to Heaven",
                    'album': 'Adorn',
                    'track_name': 'Closer',
                    'acousticness': 0.976,
                    'danceability': 0.168,
                    'duration_ms': 164135,
                    'energy': 0.526,
                    'instrumentalness': 0.958,
                    'key': 6,
                    'liveness': 0.153,
                    'loudness': -8.495,
                    'mode': 0,
                    'speechiness': 0.0456,
                    'tempo': 76.89,
                    'time_signature': 3,
                    'valence': 0.0706
                },
            ]
        """
        album = self.sp.album(album_url)

        tracklist = []
        for track in self.sp.album_tracks(album_url)["items"]:
            features = self.get_track_features(track["id"])
            track_data = {
                "artist": self.extract_artist(album),
                "album": album["name"],
                "track_name": track["name"],
                **features,
            }
            tracklist.append(track_data)

        return tracklist

    def extract_artist(self, album_data: dict) -> str:
        """Get artist name from an album's JSON data."""
        try:
            return album_data["artists"][0]["name"]
        except (KeyError, IndexError):
            print(f'Could not find artist for album {album_data["name"]}')

    def get_track_features(self, track_id: str) -> dict:
        """
        Get a track's audio features, ignoring the unecessary URLs and IDs.

        https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-audio-features
        """
        features = self.sp.audio_features(track_id)[0]

        # delete unecessary data
        del features["id"]
        del features["analysis_url"]
        del features["track_href"]
        del features["type"]
        del features["uri"]

        return features

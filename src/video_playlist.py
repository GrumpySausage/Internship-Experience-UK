"""A video playlist class."""

from typing import Sequence
from .video import Video


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, playlist_id):
        self._playlist_id = playlist_id
        self._videos = {}

    @property
    def playlist_id(self) -> str:
        """Returns title of a playlist."""
        return self._playlist_id

    @property
    def videos(self) -> Sequence[Video]:
        """Returns title of a video."""
        return list(self._videos.values())

    def add_video(self, video) -> bool:
        if video.video_id in self._videos:
            return False
        self._videos[video.video_id] = video
        return True

    def remove_video(self, video_id) -> bool:
        if video_id not in self._videos:
            return False
        self._videos.pop(video_id)
        return True

    def clear(self):
        self._videos.clear()


class PlaylistLibrary:
    def __init__(self):
        self._playlists = {}

    def create_playlist(self, playlist_name) -> bool:
        if playlist_name.lower() in self._playlists:
            print("Unable to create playlist as a playlist with the same name already exists")
            return False
        self._playlists[playlist_name.lower()] = Playlist(playlist_name)
        return True

    def delete_playlist(self, playlist_name) -> bool:
        if playlist_name.lower() not in self._playlists:
            print(f"Unable to delete playlist {playlist_name} as playlist doesn't exist")
            return False
        self._playlists.pop(playlist_name.lower())
        print("Successfully deleted playlist:", playlist_name)
        return True

    def get_all_playlists(self) -> Sequence[Playlist]:
        return list(self._playlists.values())

    def get_playlist(self, playlist_name) -> Playlist:
        return self._playlists.get(playlist_name.lower(), None)

"""A video player class."""
import random
from .video_library import VideoLibrary
from .video_playlist import PlaylistLibrary


class PlayState:
    """A class used to represent the PlayState."""

    def __init__(self, v=None):
        self.video = v
        self.paused = False


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self._current_playing = None
        self._playlists = PlaylistLibrary()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the current library")

    def show_all_videos(self):
        """Returns all videos"""
        print("All available videos in current library:")
        for vid in sorted(self._video_library.get_all_videos(), key=lambda v: v.title):
            print(f" {vid.format}")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)
        if video is None:
            print("Unfortunately this video does not exist and can't be played")
            return
        if video.flag is not None:
            print(f"Unable to play current video as it is flagged as for being {video.flag}")
            return
        if self._current_playing:
            self.stop_video()
        print("Playing current video:", video.title)
        self._current_playing = PlayState(video)

    def stop_video(self):
        """Stops the current video."""

        if self._current_playing is None:
            print("Unable to stop video as no video is currently being played")
            return
        print("Stopping current video:", self._current_playing.video.title)
        self._current_playing = None
        self._paused = False

    def play_random_video(self):
        """Plays a random video from the video library."""

        videos = self._video_library.get_all_unflagged_videos()
        if not videos:
            print("No available videos")
            return
        vid = random.choice(videos)
        self.play_video(vid.video_id)

    def pause_video(self):
        """Pauses the current video."""

        if self._current_playing is None:
            print("Unable to pause video as no video is currently being played")
            return
        if self._current_playing.paused:
            print("Video is already paused:", self._current_playing.video.title)
            return
        self._current_playing.paused = True
        print("Pausing current video:", self._current_playing.video.title)

    def continue_video(self):
        """Resumes playing the current video."""

        if self._current_playing is None:
            print("Unable to resume video as no video is being played")
            return
        if not self._current_playing.paused:
            print("Video is already playing")
            return
        print("Resuming current video:", self._current_playing.video.title)
        self._current_playing.paused = False

    def show_playing(self):
        """Displays video currently playing."""

        if self._current_playing is None:
            print("No video currently being played")
            return
        print("Currently playing:", self._current_playing.video.format,
              "-PAUSED" * self._current_playing.paused)

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if not self._playlists.create_playlist(playlist_name):
            return
        print("New playlist created successfully:", playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        p = self._playlists.get_playlist(playlist_name)
        if p is None:
            print(f"Unable to add video to playlist: {playlist_name}, as specified playlist doesn't exist")
            return
        vid = self._video_library.get_video(video_id)
        if vid is None:
            print(f"Unable to add video to playlist: {playlist_name}, as selected video doesn't exist")
            return
        if vid.flag:
            print(f"Unable to add video to playlist: {playlist_name}, "
                  f"as selected video is currently flagged for being {vid.flag}")
            return
        if not p.add_video(vid):
            print(f"Unable to add video to playlist: {playlist_name}, as selected video is already in this playlist")
            return
        print(f"The video {vid.title} was successfully added to playlist: {playlist_name}")

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        p = self._playlists.get_playlist(playlist_name)
        if p is None:
            print(f"Unable to display playlist {playlist_name} as specified playlist doesn't exist")
            return
        print("Displaying playlist:", playlist_name)
        if not p.videos:
            print("There are currently no videos in this playlist")
            return
        for vid in p.videos:
            print(f"{vid.format}")

    def show_all_playlists(self):
        """Display all playlists."""

        pl = self._playlists.get_all_playlists()
        if not pl:
            print("No existing playlists")
            return
        print("Displaying all playlists:")
        for p in sorted(pl, key=lambda p: p.playlist_id):
            print(f"{p.playlist_id} ({len(p.videos)} videos)")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        p = self._playlists.get_playlist(playlist_name)
        if p is None:
            print(f"Unable to remove video from {playlist_name} as specified playlist doesn't exist")
            return
        vid = self._video_library.get_video(video_id)
        if vid is None:
            print(f"Unable to remove video from {playlist_name} as selected video doesn't exist")
            return
        if not p.remove_video(video_id):
            print(f"Unable to remove video from {playlist_name} as selected video isn't in this playlist")
            return
        print(f"Removed video from {playlist_name}: {vid.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        p = self._playlists.get_playlist(playlist_name)
        if p is None:
            print(f"Unable to clear playlist {playlist_name} as specified playlist doesn't exist")
            return
        p.clear()
        print(f"All videos from playlist {playlist_name} were removed successfully")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        self._playlists.delete_playlist(playlist_name)

    def search_selection(self, search_term, results):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query used to search.
            results: lists videos, search result
        """
        results = sorted(results, key=lambda v: v.title)
        if not results:
            print(f"No results match search for {search_term}, don't forget the #")
            return
        print(f"Results for {search_term}:")
        for i, vid in enumerate(results):
            print(f"  {i + 1}) {vid.format}")
        print("Would you like to play any of the above? If yes, please specify the number of the video.")
        print("An invalid number means you don't want to.")
        selection = input()
        if not selection.isnumeric():
            return
        select = int(selection)
        if select < 1 or select > len(results):
            return
        self.play_video(results[select - 1].video_id)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        self.search_selection(
            search_term,
            filter(
                lambda v: search_term.lower() in v.title.lower(),
                self._video_library.get_all_unflagged_videos()))

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        self.search_selection(
            video_tag,
            filter(
                lambda v: video_tag.lower() in {t.lower() for t in v.tags},
                self._video_library.get_all_unflagged_videos()))

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        vid = self._video_library.get_video(video_id)
        if not vid:
            print("Unable to flag video as selected video doesn't exist")
            return
        if vid.flag is not None:
            print("Unable to flag an already flagged video")
            return
        vid.set_flag(flag_reason)
        print(f"{vid.title} was successfully flagged for being {flag_reason}")
        if self._current_playing and self._current_playing.video.video_id == video_id:
            self.stop_video()

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        vid = self._video_library.get_video(video_id)
        if not self._video_library.get_video(video_id):
            print("Unable to remove flag as specified video doesn't exist")
            return
        if not vid.flag:
            print("Unable to remove flag from this video as it is not currently flagged")
            return
        print("Flag was successfully removed from this video:", vid.title)
        vid.set_flag(None)

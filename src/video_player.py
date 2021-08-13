"""A video player class."""

from .video_library import VideoLibrary
import random
from .video_playlist import Playlist

class VideoPlayer:

    """A class used to represent a Video Player."""
    def __init__(self):
        self._video_library = VideoLibrary()
        self.current_video_ids = {}
        self.playlists = {}
        self.all_videos = self._video_library.get_all_videos()

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""

        all_videos = self.all_videos
        all_videos.sort(key=lambda v: v.title)

        print(f"Here's a list of all available videos:")
        for video in all_videos:
            print(f" {video.title} ({video.video_id}) [{' '.join(list(video.tags))}]")


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """

        new_video = self._video_library.get_video(video_id)

        if not new_video:
            print(f"Cannot play video: Video does not exist")
            return

        current_video_id = self.current_video_ids.get("current_video_id")
        if current_video_id:
            self.stop_video()
            self.current_video_ids["current_video_id"] = new_video.video_id
            self.current_video_ids["is_current_video_playing"] = True
            print(f"Playing video: {new_video.title}")
        else:
            self.current_video_ids["current_video_id"] = new_video.video_id
            self.current_video_ids["is_current_video_playing"] = True
            print(f"Playing video: {new_video.title}")


    def stop_video(self):
        """Stops the current video."""

        current_video_id = self.current_video_ids.get("current_video_id")
        if not current_video_id:
            return print("Cannot stop video: No video is currently playing")
        current_video = self._video_library.get_video(current_video_id)
        self.current_video_ids["current_video_id"] = None
        self.current_video_ids["is_current_video_playing"] = None
        print(f"Stopping video: {current_video.title}")

    def play_random_video(self):
        """Plays a random video from the video library."""

        all_videos = self.all_videos
        random_video = random.choice(all_videos)
        self.play_video(random_video.video_id)

    def pause_video(self):
        """Pauses the current video."""

        current_video_id = self.current_video_ids.get("current_video_id")
        if not current_video_id:
            return print(f"Cannot pause video: No video is currently playing")
        current_video = self._video_library.get_video(current_video_id)
        if self.current_video_ids["is_current_video_playing"]:
            self.current_video_ids["is_current_video_playing"] = False
            print(f"Pausing video: {current_video.title}")
        else:
            print(f"Video already paused: {current_video.title}")


    def continue_video(self):
        """Resumes playing the current video."""

        current_video_id = self.current_video_ids.get("current_video_id")
        if not current_video_id:
            return print(f"Cannot continue video: No video is currently playing")
        current_video = self._video_library.get_video(current_video_id)
        if self.current_video_ids["is_current_video_playing"] is False:
            self.current_video_ids["is_current_video_playing"] = True
            print(f"Continuing video: {current_video.title}")
        else:
            print(f"Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        current_video_id = self.current_video_ids.get("current_video_id")
        if not current_video_id:
            return print(f"No video is currently playing")
        current_video = self._video_library.get_video(current_video_id)
        if self.current_video_ids["is_current_video_playing"]:
            print(f"Currently playing: {str(current_video)}")
        else:
            print(f"Currently playing: {str(current_video)} - PAUSED")

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        new_playlist_id = playlist_name.lower()
        if new_playlist_id in self.playlists.keys():
            return print(f"Cannot create playlist: A playlist with the same name already exists")
        else:
            new_playlist = Playlist(playlist_name)
            self.playlists[new_playlist_id] = new_playlist
            print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        playlist_id = playlist_name.lower()
        if playlist_id not in self.playlists.keys():
            return print(f"Cannot add video to {playlist_id}: Playlist does not exist")

        if not self._video_library.get_video(video_id):
            return print(f"Cannot add video to {playlist_name}: Video does not exist")

        if video_id in self.playlists[playlist_id].videos:
            return print(f"Cannot add video to {playlist_name}: Video already added")

        video = self._video_library.get_video(video_id)
        self.playlists[playlist_id].videos.append(video_id)
        return print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists.keys()) <= 0:
            return print(f"No playlists exist yet")
        else:
            all_playlists = sorted(self.playlists.keys())
            print(f"Showing all playlists:")
            for playlist in all_playlists:
                print(self.playlists.get(playlist).name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist_id = playlist_name.lower()
        if playlist_id not in self.playlists.keys():
            return print(f"Cannot show playlist {playlist_name}: Playlist does not exist")

        videos = self.playlists.get(playlist_id).videos

        if len(videos) == 0:
            print(f"Showing playlist: {playlist_name}")
            print("No videos here yet")
            return

        print(f"Showing playlist: {playlist_name}")
        for video_id in videos:
            print(self._video_library.get_video(video_id))

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        playlist_id = playlist_name.lower()

        if playlist_id not in self.playlists.keys():
            return print(f"Cannot remove video from {playlist_name}: Playlist does not exist")

        if not self._video_library.get_video(video_id):
            return print(f"Cannot remove video from {playlist_name}: Video does not exist")

        if video_id not in self.playlists[playlist_id].videos:
            return print(f"Cannot remove video from {playlist_name}: Video is not in playlist")

        video = self._video_library.get_video(video_id)

        self.playlists[playlist_id].videos.remove(video_id)
        return print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist_id = playlist_name.lower()
        if playlist_id not in self.playlists.keys():
            return print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")

        self.playlists.get(playlist_id).videos = []
        print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        playlist_id = playlist_name.lower()

        if playlist_id not in self.playlists.keys():
            return print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")

        self.playlists.pop(playlist_id)
        print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """

        all_videos = self.all_videos
        matched_videos = []
        for video in all_videos:
            if search_term.lower() in video.title.lower():
                matched_videos.append(video)

        matched_videos.sort(key=lambda mv: mv.title)

        if len(matched_videos) == 0:
            print(f"No search results for {search_term}")
        else:
            print(f"Here are the results for {search_term}:")
            for i in range(len(matched_videos)):
                print(f"({i + 1}) {matched_videos[i].title} {matched_videos[i].video_id} [{' '.join(matched_videos[i].tags)}]")

            print(f"Would you like to play any of the above? If yes, specify the number of the video.")
            print(f"If your answer is not a valid number, we will assume it's a no.")

            video_number = input()
            if video_number.isdigit() and 1 <= len(matched_videos) >= int(video_number):
                self.play_video(matched_videos[int(video_number) - 1].video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        all_videos = self.all_videos
        matched_videos = []

        for video in all_videos:
            if video_tag.lower() in video.tags:
                matched_videos.append(video)

        matched_videos.sort(key=lambda mv: mv.title)

        if len(matched_videos) == 0:
            print(f"No search results for {video_tag}")
        else:
            print(f"Here are the results for {video_tag}:")
            for i in range(len(matched_videos)):
                print(f"({i + 1}) {matched_videos[i].title} ({matched_videos[i].video_id}) [{' '.join(matched_videos[i].tags)}]")

            print(f"Would you like to play any of the above? If yes, specify the number of the video.")
            print(f"If your answer is not a valid number, we will assume it's a no.")

            video_number = input()
            if video_number.isdigit() and 1 <= len(matched_videos) >= int(video_number):
                self.play_video(matched_videos[int(video_number) - 1].video_id)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        print("flag_video needs implementation")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        print("allow_video needs implementation")

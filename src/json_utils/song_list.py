import json
from os import path, rename

from yt_utils import download_playlist_videos_info

class SongList:
    # json_file_path = path to the most recent song_list
    # song_info_list = list of song info read from json_file_path

    def __init__(self, mirror_path :str, action_time :str) -> None:
        self.mirror_path = mirror_path
        self.action_time = action_time

    def create_list(self, song_info_list :list[dict]) -> None:
        self.json_file_path = path.join(self.mirror_path, "song_list/INITIAL.json")

        if path.exists(self.json_file_path):
            raise Exception("Use of initial song list creation method when INITIAL.json already exists")


        self.song_info_list = []

        # add extra fields
        for song_info in song_info_list:
            song_info["duplicate"] = False
            song_info["resource"] = False
            song_info["file_name"] = f"{song_info['title']}.mp3"
            self.song_info_list.append(song_info)
        



    def read_list(self) -> None:
        self.json_file_path = path.join(self.mirror_path, "song_list/CURRENT.json")
        if not path.exists(self.json_file_path):
            self.json_file_path = path.join(self.mirror_path, "song_list/INITIAL.json")
        if not path.exists(self.json_file_path):
            raise Exception("No song_list found")

        with open(self.json_file_path, "r") as f:
            self.song_info_list = json.load(f)

        

    def update_list(self) -> None:
        current_song_info_list = self.read_list()

        updated_song_info_list = download_playlist_videos_info(self.mirror_path)

        merged_song_info_list :list[dict] = []
        to_append_list :list[dict] = []

        matched_songs = set()

        for new_song in updated_song_info_list:
            new_song_id = new_song["url"].split("=")[-1]
            for current_song in current_song_info_list:

                current_song_id = current_song["url"].split("=")[-1]

                if current_song_id in matched_songs:
                    continue

                if new_song_id == current_song_id:
                    merged_song_info_list.append(current_song)
                    
                    matched_songs.add(current_song_id)
        
        merged_song_info_list.extend(to_append_list)
        self.song_info_list = merged_song_info_list

    def save_list(self) -> None:
        self.json_file_path = path.join(self.mirror_path, "song_list/INITIAL.json")
        if path.exists(self.json_file_path)
            self.json_file_path = path.join(self.mirror_path, "song_list/CURRENT.json")
        if path.exists(self.json_file_path):
            rename(self.json_file_path, path.join(self.mirror_path, f"{self.action_time}.json"))

        with open(self.json_file_path, "w") as f:
            json.dump(self.song_info_list, f, indent=4, ensure_ascii=False)

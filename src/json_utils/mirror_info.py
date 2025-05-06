import json
from datetime import datetime
from os import path

from .info_file import InfoFile

from yt_utils import download_playlist_info

class MirrorInfo(InfoFile):
    def __init__(self, mirror_path :str, action_time :str) -> None:
        super().__init__(mirror_path, action_time)

        self.json_file_path = path.join(self.mirror_path, "mirror_info.json")

    def __eq__(self):
        return self.mirror_info_dict

    def generate_mirror_info(self, playlist_info :dict) -> str:

        if not path.exists(self.json_file_path):

            mirror_info = {
                "title": playlist_info["title"],
                "url": playlist_info["url"],
                "video_count": playlist_info["video_count"],
                "mirror_creation_time": self.action_time,
                "mirror_last_updated": self.action_time
            }

            with open(self.json_file_path, 'w') as f:
                json.dump(mirror_info, f, indent=4)
            
            self.mirror_info_dict = mirror_info
        
        else:
            raise Exception("mirror_info.json already exists")

    def update_mirror_info(self):
        self.read_mirror_info

        new_playlist_info = download_playlist_info(self.mirror_info_dict["url"])

        self.mirror_info_dict["video_count"] = new_playlist_info["video_count"]
        self.mirror_info_dict["mirror_last_updated"] = self.action_time

        with open(self.json_file_path, 'w') as f:
            json.dump(self.mirror_info_dict, f, indent=4)


    def read_mirror_info(self) -> dict:
        json_file_path = path.join(self.mirror_path, "mirror_info.json")

        if not path.exists(json_file_path):
            raise Exception("No mirror_info.json found")

        with open(json_file_path, 'r') as f:
            mirror_info = json.load(f)

        self.mirror_info_dict = mirror_info
import json
from datetime import datetime
from os import path

def generate_mirror_info(playlist_info :dict, mirror_path :str, action_time :str) -> str:
    json_file_path = path.join(mirror_path, "mirror_info.json")
    
    if not path.exists(json_file_path):

        mirror_info = {
            "title": playlist_info["title"],
            "url": playlist_info["url"],
            "video_count": playlist_info["video_count"],
            "mirror_creation_time": action_time,
            "mirror_last_updated": action_time
        }
        
        with open(json_file_path, 'w') as f:
            json.dump(mirror_info, f, indent=4)

    return json_file_path

def read_mirror_info(mirror_path :str) -> dict:
    json_file_path = path.join(mirror_path, "mirror_info.json")

    if not path.exists(json_file_path):
        raise Exception("No mirror_info.json found")

    with open(json_file_path, 'r') as f:
        mirror_info = json.load(f)

    return mirror_info
import json
from os import path


def song_list_json_generator(video_info_list :list, mirror_path :str) -> str:
    
    json_song_list = []

    # add extra fields
    for video_info in video_info_list:
        video_info["path"] = None
        video_info["duplicate"] = False
        video_info["resource"] = False
        json_song_list.append(video_info)

    json_file_path = path.join(mirror_path, "INITIAL.json")

    if not path.exists(json_file_path):
        with open(json_file_path, "w") as f:
            json.dump(json_song_list, f, indent=4, ensure_ascii=False)

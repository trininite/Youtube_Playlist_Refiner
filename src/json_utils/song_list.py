import json
from os import path, rename


def generate_song_list(video_info_list :list, mirror_path :str, action_time :str) -> str:
    
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
    
    else:
        json_file_path = path.join(mirror_path, "CURRENT.json")
        if path.exists(json_file_path):
            rename(json_file_path, path.join(mirror_path, f"{action_time}.json"))

        with open(json_file_path, "w") as f:
            json.dump(json_song_list, f, indent=4, ensure_ascii=False)

    


def read_song_list(mirror_path :str) -> list[dict]:
    if not path.exists(path.join(mirror_path, "song_list/CURRENT.json")):
        song_list = path.join(mirror_path, "song_list/INITIAL.json")
    else:
        song_list = path.join(mirror_path, "song_list/CURRENT.json")

    with open(song_list, "r") as f:
        song_list = json.load(f)

    return song_list
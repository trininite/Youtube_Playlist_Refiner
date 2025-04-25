import json
from os import path as os_path
from datetime import datetime

from yt_utils import download_playlist_videos_info


def song_list_json_generator(playlist_url :str, mirror_path :str) -> str:
    
    json_song_list = []

    song_info_list = download_playlist_videos_info(playlist_url)
    
    # add the resource flag to the object then add it to the list
    for song_info in song_info_list:
        song_info["mark_for_resource"] = False
        json_song_list.append(song_info)

    # create the INITIAL instance of the song list if it doesn't exist
    if not os_path.exists(os_path.join(mirror_path, "INITIAL.json")):
        song_list_name = "INITIAL"
    else:
        song_list_name = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(os_path.join(mirror_path, f"{song_list_name}.json"), "w") as f:
        json.dump(json_song_list, f, indent=4, ensure_ascii=False)

    
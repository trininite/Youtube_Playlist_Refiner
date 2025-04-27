import os
#import shutil
#import sys

from json_utils import generate_mirror_info
from json_utils import generate_song_list

from yt_utils import download_playlist_info
from yt_utils import download_playlist_videos_info

from .mirror_cache import create_mirror_cache


def create_mirror(action_time :str) -> str:
    """
    Creates a directory at mirror_path/title.

    Parameters:
        None    
    
    Returns:
        str: Full path to the created directory.
    """
    playlist_url :str = input("Enter the !FULL! URL of the playlist you want to mirror: ")
    playlist_info :dict = download_playlist_info(playlist_url)
    del playlist_url

    # parent directory of the mirror
    mirror_parent_path :str = input("Enter the !ABSOLUTE! path of where you want the mirror folder: ")

    # actual location of the mirror
    mirror_path :str = os.path.join(mirror_parent_path, playlist_info["title"])
    # dont overwrite existing mirror
    try:
        os.makedirs(mirror_path, exist_ok=False)
    except OSError as e:
        print(e)
        print("Error creating mirror folder. A folder with the same name may already exist.")

    # create mirror_info.json
    generate_mirror_info(playlist_info, mirror_path, action_time)

    # create the song history folder
    # contains all the downloaded songs in dated json files
    # first list will be named INITIAL
    # current list will be named CURRENT
    # all previous lists, excluding the first, will be named YYYY-MM-DD_HH-MM-SS
    song_list_history_path :str = os.path.join(mirror_path, "song_list")
    try:
        os.makedirs(song_list_history_path, exist_ok=False)
    except OSError as e:
        print(e)
        print("Error creating song list history folder. A folder with the same name may already exist.")

    video_info_list = download_playlist_videos_info(playlist_info["url"])

    generate_song_list(video_info_list, song_list_history_path)

    create_mirror_cache(mirror_path)

    return mirror_path

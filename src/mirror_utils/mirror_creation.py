import os
#import shutil
#import sys

from json_utils import generate_mirror_info
from json_utils import SongList

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
    if "~" in mirror_parent_path:
        mirror_parent_path = os.path.expanduser(mirror_parent_path)

    assert os.path.exists(mirror_parent_path)

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
    song_list_dir_path :str = os.path.join(mirror_path, "song_list")

    os.makedirs(song_list_dir_path, exist_ok=True)

    song_info_list = download_playlist_videos_info(playlist_info["url"])

    song_list = SongList(mirror_path, action_time)
    song_list.create_list(song_info_list)
    song_list.save_list()

    create_mirror_cache(mirror_path)

    return mirror_path

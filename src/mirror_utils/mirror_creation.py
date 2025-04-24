import os
#import shutil
#import sys

from json_utils import mirror_info_json_generator

from yt_utils import download_playlist_info


def create_mirror() -> str:
    """
    Creates a directory at mirror_path/title.

    Parameters:
        None    
    
    Returns:
        str: Full path to the created directory.
    """
    url :str = input("Enter the !FULL! URL of the playlist you want to mirror: ")
    playlist_info :dict = download_playlist_info(url)
    playlist_title :str = playlist_info['title']
    video_count :int = playlist_info['video_count']

    # parent directory of the mirror
    mirror_parent_path :str = input("Enter the !ABSOLUTE! path of where you want the mirror folder: ")

    # actual location of the mirror
    mirror_path :str = os.path.join(mirror_parent_path, playlist_info['title'])
    # dont overwrite existing mirror
    try:
        os.makedirs(mirror_path, exist_ok=False)
    except OSError as e:
        print(e)
        print("Error creating mirror folder. A folder with the same name may already exist.")

    # create mirror_info.json
    mirror_info_json_generator(playlist_title, url, mirror_path, video_count)

    # create the song history folder
    # contains all the downloaded songs in dated json files
    song_list_history_path :str = os.path.join(mirror_path, "song_list_history")
    os.makedirs(song_list_history_path, exist_ok=True)

    return mirror_path

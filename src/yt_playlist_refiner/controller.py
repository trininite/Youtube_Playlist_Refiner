# from pathlib import Path
from os import path as os_path

from enum import Enum
from dataclasses import dataclass, asdict

from datetime import datetime

from utils import yes_no, resolve_path, valid_path


from mirror_cache import CacheManager

from mirror_controller import MirrorController

from youtube_api import YoutubeAPI


class Operations(Enum):
    CREATE = "CREATE"

    MODIFY_ADD = "ADD"
    MODIFY_REMOVE = "REMOVE"
    MODIFY_OUTPUT_FILENAME = "OUTPUT_FILENAME"

    SYNC_L2R = "L2R"
    SYNC_R2L = "R2L"
    SYNC_MERGE = "MERGE"

#@dataclass
#class 



def greet() -> None:
    print("Welcome to Youtube Playlist Refiner")


def get_new_mirror_playlist_url():
    while True:
        print("Enter the !FULL YOUTUBE PLAYLIST URL! (Youtube Music URLs yet not supported)")
        mirror_remote_url = input(">> ")
        if not mirror_remote_url: 
            print("Empty input\n\n")
            continue

        break

def get_new_mirror_path(mirror_folder_path :str) -> str:
    while True:
        #TODO Error handling
        print("Enter the !FULL PATH! where the mirror should be stored")
        print("A folder w/ the name of the remote playlist will be created at this path")
        mirror_folder_path = resolve_path(input(">> "))
        if not valid_path(mirror_folder_path):
            print("invalid path, looping...")
            continue
        break


def get_sync_operation() -> str:
    while True:
        print("What would you like to do?")
        print("[1] - Push Local to Remote (Overwrite)")
        print("[2] - Pull Remote to Local (Overwrite)")
        print("[3] - Merge Local and Remote")

        try:
            opr = int(input())
            if opr not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print(f"Invalid input '{opr}'\n\n\n")
            print(f"Retry?")
            do_retry :bool = yes_no(assume_yes=True)
            if do_retry:
                continue

        match opr:
            case 1:
                return Operations.SYNC_L2R
            case 2:
                return Operations.SYNC_R2L
            case 3:
                return Operations.SYNC_MERGE


def get_update_operation() -> str:
    while True:
        print("What would you like to do?")
        print("[1] - Add Song(s)")
        print("[2] - Remove Song(s)")
        print("[3] - Modify Output Filename(s) of Song(s)")

        try:
            opr = int(input())
            if opr not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print(f"Invalid input '{opr}'\n\n\n")
            print(f"Retry?")
            do_retry :bool = yes_no(assume_yes=True)
            if do_retry:
                continue

        match opr:
            case 1:
                return Operations.MODIFY_ADD
            case 2:
                return Operations.MODIFY_REMOVE
            case 3:
                return Operations.MODIFY_OUTPUT_FILENAME        


def get_operation() -> str:
    while True:
        print("What do you want to do?")
        print("[1] - Create Mirror")
        print("[2] - Sync Mirror")
        print("[3] - Modify Mirror")

        # get base operation in # form. ensure its a valid input; handle errors if not.
        try:
            opr = int(input())
            if opr not in [1, 2, 3]:
                raise ValueError
        except ValueError:
            print(f"Invalid input '{opr}'\n\n\n")
            print(f"Retry?")
            do_retry :bool = yes_no(assume_yes=True)
            if do_retry:
                continue

            quit()
        
        match opr:
            case 1:
                return Operations.CREATE
            case 2:
                return get_sync_operation()
            case 3:
                return get_update_operation()
        


class Controller:
    def __init__(self):
        self._validate_filesystem(self)
        
    def run(self):
        self.action_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        greet()
        operation = get_operation()

        match operation:
            case Operations.CREATE:
                self._create_mirror()

            case Operations.MODIFY_ADD:
                ...
            case Operations.MODIFY_REMOVE:
                ...
            case Operations.MODIFY_OUTPUT_FILENAME:
                ...

            case Operations.SYNC_L2R:
                ...
            case Operations.SYNC_R2L:
                ...
            case Operations.SYNC_MERGE:
                ...

    def _validate_filesystem(self):
        required_files = [
            "~/.cache/yt_playlist_refiner/mirror_paths.txt",
            "~/.cache/yt_playlist_refiner/API_KEY.txt"
        ]
        
        missing_paths = []

        for path in required_files:
            if not valid_path(path):
                missing_paths.append(path)

        if missing_paths:
            print("The following required paths are missing:")
            for path in missing_paths:
                print(f"- {path}")
            print("Please create them before proceeding.")
            raise FileExistsError

    def _load_api_key(self):
        api_file_path = "src/api_secrets/DEV_YTAPI_SECRET.txt"
        with open(api_file_path, mode="r", encoding="UTF+8") as f:
            self._api_key = f.readlines[0]


    def _create_mirror(self):
        # assumptions:
        #   the cache is already created
        #   new mirror doesnt exist yet
        #   user has provided a valid api key

        # switch to oauth2 authentication (painful (help))
        self._load_api_key()

        #TODO start using pathlib everywhere 
        #new_mirror_folder_path :Path = get_new_mirror_path()
        new_mirror_playlist_url :str = get_new_mirror_playlist_url()
        new_mirror_parent_path :str = get_new_mirror_path()


        yt_api = YoutubeAPI(self._api_key, new_mirror_playlist_url)
        playlist_title = yt_api.title
        song_count = yt_api.song_count
        etag = yt_api.etag


        new_mirror_path :str = os_path.join(new_mirror_parent_path, playlist_title)

        cache_man = CacheManager()

        if not cache_man.mirror_path_unique(new_mirror_path):
            raise FileExistsError(f"mirror for {new_mirror_path} already exists")

        mirror_con = MirrorController(
            mirror_path=new_mirror_parent_path,
            api_key=self._api_key,
            action_time=self.action_time,
            playlist_url=new_mirror_playlist_url
        )

        cache_man.add_mirror_path(new_mirror_path)
        cache_man._update_cache()

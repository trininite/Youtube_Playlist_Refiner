#TODO implement pathlib  
from pathlib import Path

import json

from os import path

from dataclasses import dataclass

from youtube_api import YoutubeAPI

from mirror_cache import CacheManager

@dataclass
class MirrorInfo:
    title: str | None = None
    url: str | None = None
    song_count: int | None = None #NOTE this value isnt very critical, the working song_count will be generated from 
    etag: str | None = None
    mirror_creation_time: str | None = None
    mirror_last_updated: str | None = None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class MirrorController:
    def __init__(
        self,
        mirror_path:str,
        yt_api:YoutubeAPI,
        action_time:str,
        playlist_url:str=None
        ):

        self.mirror_info = MirrorInfo()

        #NOTE a playlist url is only passed when creating a mirror
        creating :bool = bool(playlist_url)

        # arg vars
        self._mirror_path :Path = Path(mirror_path).expanduser().absolute()
        self._yt_api = yt_api

        

        if creating:
            self.mirror_info.url = playlist_url
            self._sync_mirror_info()
        if not creating:
            self._read_mirror_info_file()

        try:
            assert self._yt_api._playlist_valid()
            assert self.mirror_info.title
            assert self.mirror_info.song_count
            assert self.mirror_info.etag
        except AssertionError as e:
            print("couldnt validate playlist url\n",e)
            return None

                

    @property
    def mirror_info_filepath(self) -> Path:
        filename :Path = Path("mirror_info.json")

        filepath :Path = self._mirror_path.joinpath(filename)

        filepath :Path = filepath.expanduser().absolute()

        return filepath
    

    def _generate_mirror_files(self):
        # mkdir self._mirror_path
        # touch self._mirror_path / mirror_info.json
        try:
            self._mirror_path.mkdir(parents=True, exist_ok=False)
            self._mirror_path
        except FileExistsError as e:
            error_message :str = f"mirror at {self._mirror_path} already exists"
            print(e(error_message))
            quit(code=1)
    
        #NOTE maybe allow SongList to handle below
        # mkdir self._mirror_path / song_list
        # touch self._mirror_path / song_list / INITIAL.json
        ...

    
    def _read_mirror_info_file(self):
        if


        with open(self.mirror_info_filepath, "r", encoding="utf+8") as f:
            stored_mirror_info = json.load(f)

        self.mirror_info.title = stored_mirror_info["title"]
        self.mirror_info.url = stored_mirror_info["url"]
        self.mirror_info.song_count = stored_mirror_info["song_count"]
        self.mirror_info.etag = stored_mirror_info["etag"]
        self.mirror_info.mirror_creation_time = stored_mirror_info["mirror_creation_time"]
        self.mirror_info.mirror_last_updated = stored_mirror_info["mirror_last_updated"]


    def _write_mirror_info_file(self):
        with open(self.mirror_info_filepath, "w", encoding="utf+8") as f:
            self.mirror_info.mirror_last_updated = self.action_time
            json.dump(self.mirror_info, f, indent=4)
        ...


    def _sync_mirror_info(self):
        # sync mirror info to playlist 
        #NOTE (maybe have a local to remote title change function???? :O)
        self._yt_api.sync_playlist_info()

        self.mirror_info.title = self._yt_api.title
        self.mirror_info.song_count = self._yt_api.song_count
        self.mirror_info.etag = self._yt_api.etag
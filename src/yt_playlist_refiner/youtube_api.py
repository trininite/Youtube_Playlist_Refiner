from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from enum import Enum

class PlayListErrors(Enum):
    LIST = {
        400 :tuple[str] ("playlistOperationUnsupported"),
        403 :tuple[str] ("channelClosed", "channelSuspended", "playlistForbidden"),
        404 :tuple[str] ("channelNotFound", "playlistNotFound")
    }

class VideosErrors(Enum):
    LIST :dict = {
        400 :tuple[str] ("videoChartNotFound"),
        403 :tuple[str] ("forbidden"),
        404 :tuple[str] ("videoNotFound")
    }



#TODO make singleton
class YoutubeAPI:
    def __init__(self, api_key:str, playlist_url:str):
        self._api_key :str = api_key

        self.youtube_service = build("youtube", "v3", developerKey=self._api_key)

        self._playlist_url :str = playlist_url

        try:
            assert self._api_key_valid()
            assert self._playlist_valid()
        except AssertionError as e:
            print(e)
            return None
        
        self.sync_playlist_info()



    #TODO cleanup error handling, shift catching to __init__
    @property
    def _api_key_valid(self) -> bool:
        # forsen
        dummy_video_id :str = "aAA77ZkKSeg"
        try:
            self.youtube_service.videos().list(
                part="status",
                id=dummy_video_id,
                maxResults=1
            ).execute()
        except HttpError as e:
            status = e.resp.status
            if status in VideosErrors.LIST.keys():
                potential_errors :tuple[str] = VideosErrors.LIST[status]
                print(e)
                print("experienced one of the following errors:")
                for error in potential_errors:
                    print(f"\t{error}")
                return False
            elif status == 200:
                return True
            else:
                print(f"unknown error {e}")
                return False

    #TODO use error enums
    @property
    def _playlist_valid(self) -> bool:
        try:
            resp = self.youtube_service.playlists().list(
                part="snippet,contentDetails",
                id=self._playlist_id,
                maxResults=1
            ).execute()
        except HttpError as e:
            status = e.resp.status
            if status in (400, 403):
                print("Invalid API key or insufficient permissions")
                return False
            raise  # re-raise unexpected errors

        return bool(resp.get("items"))



    @property
    def _playlist_id(self):
        # id is at end of url just after the only '='
        return self._playlist_url.split("=")[-1]


    def _fetch_playlist_info(self) -> dict:
        #TODO error handling
        youtube = build("youtube", "v3", developerKey=self._api_key)

        request = youtube.playlists().list(
            part="id,contentDetails,snippet",
            id=self._playlist_id
        )

        try:
            response :dict = request.execute()[0]
        except Exception as e:
            print(e)
            raise NotImplementedError



        snippet = ["snippet"]
        content_details = response["contentDetails"]

        return {
            "etag": response["snippet"],
            "title": snippet["title"],
            "song_count": content_details["itemCount"]
        }

    #TODO implement better error handling
    def sync_playlist_info(self) -> bool:
        try:
            playlist_info = self._fetch_playlist_info()

            self.etag = playlist_info["etag"]
            self.title = playlist_info["title"]
            self.song_count = playlist_info["song_count"]
        except Exception as e:
            print(e)
            return False
        else:
            return True

    def _fetch_playlist_video_info(self):
        ...

    def sync_playlist_video_info(self):
        youtube = build("youtube", "v3", developerKey=self._api_key)

        next_page_token = None

        
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=self.playlist_id,
            maxResults=10,
            pageToken=next_page_token
        )
        response = request.execute()
        
        print(json.dumps(response, indent=2))


            
    def add_song():
        ...
    
    def remove_song():
        ...

    def change_song_order(self):
        ...

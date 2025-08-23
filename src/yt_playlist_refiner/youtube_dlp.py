from yt_dlp import YoutubeDL as YTDL_base
from utils import SongInfo

class YoutubeDLP(YTDL_base):
    def __init__(self, playlist_url :str, mirror_location :str):
        super.__init__()

        self._playlist_url = playlist_url
        self._mirror_location = mirror_location

    def download_songs(self, songs :list[str]):
        ...






# otag
# https://cdn.7tv.app/emote/01GYT25QT8000DVPJKHH13026T/4x.avif
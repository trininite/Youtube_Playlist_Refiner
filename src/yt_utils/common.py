# common modules for yt_dlp utils

from yt_dlp import YoutubeDL


DEFAULT_OPTIONS = {}

def get_ydl(options=None):
    return YoutubeDL(options or DEFAULT_OPTIONS)

# otag
# https://cdn.7tv.app/emote/01GYT25QT8000DVPJKHH13026T/4x.avif
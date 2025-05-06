# utils for downloading videos and video info

from .common import get_ydl


def download_playlist_videos_info(playlist_url: str) -> list:
    """
    Downloads information for every video in a YouTube playlist.

    Parameters:
        playlist_url (str): The URL of the YouTube playlist.

    Returns:
        list: A list of dictionaries, each containing a video's title, URL,
              and the uploader's name.
    """

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': False,
    }

    videos_info = []
    with get_ydl(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

        if 'entries' in info:
            for entry in info['entries']:
                video_data = {
                    "title": entry.get("title"),
                    "url": f"https://www.youtube.com/watch?v={entry.get('id')}",
                    "channel": entry.get("uploader"),
                    "path": None,
                    "duplicate": False,
                    "resource": False
                }
                videos_info.append(video_data)

    return videos_info

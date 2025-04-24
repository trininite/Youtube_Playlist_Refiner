# utils for downloading videos and video info

from .common import get_ydl

# download info needed for creating mirror state JSON
def download_basic_video_info(video_url :str) -> dict:

    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'dump_single_json': True,
        'simulate': True
    }

    with load_ydl(ydl_opts) as ydl:
        video_info = ydl.extract_info(video_url, download=False)
        video_title = video_info['title']
        video_url = video_info['webpage_url']
        channel_name = video_info['uploader']
        channel_link = video_info['uploader_url']
        return {
            'title': video_title,
            'url': video_url,
            'channel_name': channel_name,
            'channel_link': channel_link
        }

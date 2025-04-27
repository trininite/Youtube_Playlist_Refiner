from .common import get_ydl

def download_playlist_info(playlist_url :str) -> dict:
    """
    Downloads the title and number of videos in a YouTube playlist.

    Parameters:
        playlist_url (str): The URL of the YouTube playlist.

    Returns:
        dict: A dict containing the title of the playlist and the number of videos.
    """
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
    }
    try:
        with get_ydl(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            playlist_title = playlist_info.get('title', None)
            video_count = len(playlist_info.get('entries', []))
            playlist_info :dict = {
                'title': playlist_title,
                'url': playlist_url,
                'video_count': video_count
            }
    except Exception as e:
        print(e)
        print("Error downloading playlist info. Try disabling VPN and ensure you playlist is set to public or unlisted")

    return playlist_info
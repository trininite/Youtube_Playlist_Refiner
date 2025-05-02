from .common import get_ydl
from yt_dlp.utils import DownloadError

def run_dead_link_check(song_list :list[dict]) -> list[dict]:
    updated_song_list :list[dict] = []

    dead_links :list[str] = []

    ydl_opts = {
        'format': 'best',
        'simulate': True,
        'quiet': True,
        'forceurl': True,
        'noplaylist': True,
        'no_warnings': True
    }

    with get_ydl(ydl_opts) as ydl:
        for i, song in enumerate(song_list):

            if song["duplicate"]:
                continue
            
            try:
                info = ydl.extract_info(song["url"], download=False)
                if 'url' in info:
                    updated_song_list.append(song)
                    continue
                else:
                    print(f"No URL found in meta data, open link in browser to confirm.\nURL: {song["url"]}")
                    dead :bool = True if input("[y/N]").upper() == "N" else False
                    if dead:
                        song["resource"] = True
                        dead_links.append(f"Link: {song["url"]}For Song# {i}\n{song["title"]}\n")

            except DownloadError as e:
                dead_links.append(f"Link: {song["url"]}For Song# {i}:\n{song["title"]}\n")
                song["resource"] = True

    for dead_link in dead_links:
        print(dead_link)

    return updated_song_list
    
            



import yt_dlp

from os import path, rename


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from json_utils import SongList


def download_playlist_songs(mirror_path: str, song_list :'SongList') -> None:
    songs_folder = path.join(mirror_path, "songs")

    ydl_opts = {
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    failed_songs = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, song in enumerate(song_list.song_info_list):
            if path.exists(path.join(songs_folder, song['file_name'])):
                continue

            id_path = path.join(songs_folder, f"{song['url'].split("=")[-1]}")
            ydl_opts['outtmpl'] = {"default": id_path}

            try:
                ydl.download([song['url']])

            except:
                print(f"{song['title']} failed to download, resource flag set to true")
                song_list.song_info_list[i]["resource"] = True
                failed_songs.append(song)


    if len(failed_songs) > 0:
        print(f"Failed to download {len(failed_songs)} songs, resource flag set to true")
        for song in failed_songs:
            print(f"{song["title"]}\n{song['url']}\n\n")

        return song_list
    

    

    
    

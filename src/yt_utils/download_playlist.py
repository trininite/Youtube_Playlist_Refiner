import yt_dlp

from os import path, rename



def download_playlist_songs(playlist_url: str, mirror_path: str, song_list) -> None:
    songs_folder = path.join(mirror_path, "songs")

    ydl_opts = {
        'quiet': True,
        'outtmpl': path.join(songs_folder, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
    }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

    for song in song_list.song_info_list:
        rename(path.join(songs_folder, f"{song['id']}.mp4"), path.join(songs_folder, song['file_name']))

def download_playlist_songs(mirror_path: str, song_list) -> None:
    songs_folder = path.join(mirror_path, "songs")

    ydl_opts = {
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for i, song in enumerate(song_list.song_info_list):
            id_path = path.join(songs_folder, f"{song['url'].split("=")[-1]}")
            ydl_opts['outtmpl'] = {"default": id_path}

            try:
                ydl.download([song['url']])

                rename(
                    path.join(songs_folder, f"{song['url'].split("=")[-1]}.mp3"),
                    path.join(songs_folder, song['file_name'])
                )
            except:
                print(f"{song['title']} failed to download, resource flag set to true")
                song_list.song_info_list[i]["resource"] = True

        return song_list
    

    

    
    
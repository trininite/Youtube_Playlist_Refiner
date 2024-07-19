from youtube_dl import YoutubeDL
from os import system, getcwd
import video_data_class
from logging import Logger
import re

def download_playlist_titles(playlist_url):
    ydl_opts = {
        'quiet': True,  
        'extract_flat': True,  
    }

    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(playlist_url, download=False)
        playlist_title = playlist_info.get('title', None)
        video_titles = [video['title'] for video in playlist_info['entries']]
        playlist_info = (playlist_title, video_titles)
    
    playlist_title = playlist_info[0]
    video_titles = playlist_info[1]

    return(playlist_title, video_titles)

#--- Download Functions ---





def sanitize_url(url):
    if '&' in url:
        url = url.split('&')[0]
    return url

def sanitize_title(title):
    return title.replace(" ", "_")

def bin_download_video(vdc: video_data_class, output_directory: str, logger: Logger) -> int:
    """Download a video using yt-dlp and save it to the output directory.

    Args:
        video_data_class (video_data_class): An instance of video_data_class
            containing the complete_title and video_link of the video to download.

    Returns:
        int: 1 if the video was downloaded successfully, 0 otherwise.

    """

    video_link = sanitize_url(vdc.video_link)
    output_template = f'./output/{sanitize_title(vdc.complete_title)}.mp3'
    BASE_CMD = f'lib\yt-dlp.exe -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" -x --audio-format mp3'

    
    for i in range(5):
        try:
            #print(f'{BASE_CMD} -o "{output_template}" {vdc.video_link}')
            system(f'{BASE_CMD} -o "{output_template}" {video_link}')
        except Exception as e:
            logger.error(f"Failed to download {vdc.complete_title}. Exception: {e}. Retrying...")
            if i < 4:
                continue
            return e

        break

    return 1


def _lib_download_video(video_data_class):
    custom_outtmpl = f'./output/{video_data_class.complete_title}.%(ext)s'
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': custom_outtmpl,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_data_class.video_link])


def _test_lib_download_video(title, link):
    custom_outtmpl = f'./output/{title}.%(ext)s'
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': custom_outtmpl,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


def _test_bin_download_video(title, link):
    print(getcwd())
    base_cmd = 'lib\yt-dlp.exe -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"'
    output_template = f'./output/{title}.%(ext)s'


    #system(f'{base_cmd} ')

    system(f'{base_cmd} -o "{output_template}" {link}')


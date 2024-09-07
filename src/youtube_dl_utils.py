from youtube_dl import YoutubeDL, DownloadError
from os import system, getcwd, path, chmod
from video_data_class import video_data_class
from logging import Logger
import urllib.request
import platform

def download_executable() -> None:
    """
    Downloads the yt-dlp executable for the current operating system.

    Parameters:
        None

    Returns:
        None

    Raises:
        Exception: If the current operating system is not supported.

    """
    os = platform.system()
    match os:
        case "Linux":
            if path.exists("./lib/yt-dlp_linux"):
                return
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_linux"
            urllib.request.urlretrieve(url, url.split("/")[-1])
            chmod("./lib/yt-dlp_linux", 0o755)

        case "Windows":
            if path.exists("./lib/yt-dlp.exe"):
                return
            url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
            urllib.request.urlretrieve(url, url.split("/")[-1])

        case "Mac":
            print("fuck you")
            system("reboot")
            quit()

        case _:
            raise Exception("Invalid System Type")
        
    
        

def download_playlist_titles(playlist_url :str):
    """
    Downloads the titles of a YouTube playlist.

    Parameters:
        playlist_url (str): The URL of the YouTube playlist.

    Returns:
        tuple: A tuple containing the title of the playlist and a list of video titles.
    """
    ydl_opts = {
        'quiet': True,   
        'extract_flat': True,  
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            playlist_title = playlist_info.get('title', None)
            video_titles = [video['title'] for video in playlist_info['entries']]
            playlist_info = (playlist_title, video_titles)
    except DownloadError as e:
        print(e)
        print("Error downloading playlist. Try disabling VPN")
    
    playlist_title = playlist_info[0]
    video_titles = playlist_info[1]

    return(playlist_title, video_titles)

#--- Download Functions ---



def bin_download_video(video_object: video_data_class, logger: Logger) -> int:
    """
    Download a video using yt-dlp and save it to the output directory.

    Args:
        video_data_class (video_data_class): An instance of video_data_class
            containing the complete_title and video_link of the video to download.

        logger (Logger): An instance of Logger for logging important runtime 
            information

    Returns:
        int: 1 if the video was downloaded successfully, 0 otherwise.
    """

    file_type_option = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    extraction_option = "-x --audio-format mp3"
    BASE_CMD_WINDOWS = f'lib\\yt-dlp.exe -f {file_type_option} {extraction_option}'
    BASE_CMD_BASH = f'lib/yt-dlp_linux -f {file_type_option} {extraction_option}'

    os = platform.system()
    match os:
        case "Linux":
            BASE_CMD = BASE_CMD_BASH
        case "Windows":
            BASE_CMD = BASE_CMD_WINDOWS
        case "Mac":
            print("fuck you")
            system("reboot")
            quit()
        case _:
            raise Exception("Invalid System Type")


    for i in range(5):
        try:
            #print(f'{BASE_CMD} -o "{output_template}" {video_object.video_link}')
            final_command = f'{BASE_CMD} -o {video_object.file_location} {video_object.video_link}'
            system(final_command)
        except DownloadError as e:
            logger.error(f"Failed to download {video_object.complete_title}. Exception: {e}. Retrying...")
            if i < 4:
                continue
            return e

        break

    return 1

def download_all(video_data_objects :list, logger: Logger):
    """
    Downloads a list of video data objects using the bin_download_video function.

    Args:
        video_data_objects (list): A list of video_data_class objects to be downloaded.
        logger (Logger): A logger object used for logging download information.

    Returns:
        None
    """
    video_object :video_data_class
    for video_object in video_data_objects:
        logger.info("Downloading %s", video_object.complete_title)
        res = bin_download_video(video_object, logger)

        if isinstance(res, Exception):
            logger.error("%s failed to download. Exception: %s", video_object.complete_title, res)
            video_object.file_hex, video_object.file_name = None, None
            return
        
        logger.info("%s downloaded successfully", video_object.complete_title)
        video_object.gen_hex()




# unused/old
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
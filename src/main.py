# webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# custom
from video_data_class import video_data_class
import youtube_dl_utils
import log
from user_modifcation import user_modification
from user_video_choice import user_choice

# standard
import datetime
from os import mkdir
import json


def main():
    start_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    #import config data
    main_playlist = ""
    new_playlist = "https://www.youtube.com/playlist?list=PLqj_PfKdlkzdEfBQPW1dnnGc_whfcbxO0"

    #download song titles
    new_playlist_info = youtube_dl_utils.download_playlist_titles(new_playlist)
    new_playlist_name = new_playlist_info[0]
    new_playlist_titles = new_playlist_info[1][:10]
    
    output_directory = f"./output/{new_playlist_name}_{start_time}"
    mkdir(output_directory)

    logger = log.create_logger(new_playlist_name)

    #allow user modification
    user_video_info = user_modification(new_playlist_titles, logger)
    logger.info("User modification complete")

    #TODO check for duplicates

    driver = webdriver.Firefox()
    videos = []
    # download page data, allow user to choose video, and convert it to VDC
    for info in user_video_info:

        # TODO make this a module
        # get the first 5 results for the given title and artist
        video_title = info[0]
        video_artist = info[1]

        base_search = "https://www.youtube.com/results?search_query="
        search = f"{base_search}{video_title} - {video_artist}+%22topic%22"

        driver.get(search)

        content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "contents"))
        )
        vids = content.find_elements(By.TAG_NAME, "ytd-video-renderer")[:10]

        # convert choices to VDC
        video_choices = []    
        for vid in vids:
            new_choice_vdc = video_data_class(vid, video_title, video_artist)

            video_choices.append(new_choice_vdc)

        # allow user to choose video from vdc choices and save it
        new_vdc = user_choice(video_choices, logger, choices=5)
        videos.append(new_vdc)

    # cleanup
    del(video_choices, content)
    driver.close()


    # setup metadata logging
    with open(f"{output_directory}/metadata.json", "w+") as f:
        f.close()
    metadata = []


    # download videos, hex file, log metadata
    vdc: video_data_class
    for i, vdc in enumerate(videos):
        logger.info(f"Downloading {vdc.complete_title}")
        res = youtube_dl_utils.bin_download_video(vdc, output_directory, logger)

        if isinstance(res, str):
            logger.info(f"{vdc.complete_title} downloaded successfully")
            vdc.gen_hex()
        elif isinstance(res, Exception):
            logger.error(f"{vdc.complete_title} failed to download. Exception: {res}")
            continue
    
        new_metadata = {
            "title": vdc.user_video_title,
            "artist": vdc.video_author,
            "video_link": vdc.video_link,
            "thumbnail_link": vdc.thumbnail_link,
            "channel_name": vdc.channel_name,
            "channel_link": vdc.channel_link,
            "hex": vdc.file_hex
        }

        metadata.append(new_metadata)
        
        
        """
        with open(f"{output_directory}/metadata.json", "a+") as f:
            if f.tell() == 0:
                f.write("[")
            elif f.tell() != 0 and i != len(vids) - 1:
                f.write(",")
            else:
                json.dump(metadata, f, indent=4)
                f.write("]")
                continue
            json.dump(metadata, f, indent=4)
        """

    with open(f"{output_directory}/metadata.json", "w+") as f:
        json.dump(metadata, f, indent=4)






    






if __name__ == "__main__":
    main()
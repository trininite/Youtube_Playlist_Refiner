#!usr/bin/env python3

# standard
import datetime
from os import mkdir, chdir, path
#import json

# custom
from video_data_class import video_data_class
import youtube_dl_utils
import web_driver_utils
import log
from user_modifcation import user_modification
#from user_video_choice import user_choice


def main():
    main_file_path = path.dirname(path.realpath(__file__))
    chdir(f"../{main_file_path}")

    # import config data
    # download new playlist titles
    # allow user to modify them
    # search for video using using keyword searcher
        # prompt to choose from results on zombie browser
    # convert all choices to VDC
    # download all songs
    # hex all songs
    # compile and store metadata



    start_time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    #import config data
    #main_playlist = ""
    new_playlist = "https://www.youtube.com/playlist?list=PLqj_PfKdlkzdEfBQPW1dnnGc_whfcbxO0"
    
    #check for yt-dlp binary
    youtube_dl_utils.download_executable()

    #download song titles
    new_playlist_info = youtube_dl_utils.download_playlist_titles(new_playlist)
    new_playlist_name = new_playlist_info[0]
    new_playlist_titles = new_playlist_info[1][:1] # unrefined playlist titles

    #setup logging
    if not path.exists(f"./log/"):
        mkdir(f"./log/")
        
    logger = log.create_logger(new_playlist_name)


    #create output directory
    if not path.exists(f"./output/"):
        mkdir(f"./output/")
    output_directory = f"./output/{new_playlist_name}_{start_time}"
    mkdir(output_directory)
    #create metadata file
    metadata_file = f"{output_directory}/metadata.json"
    with open(metadata_file, "w+", encoding="utf-8") as f:
        f.close()


    

    #TODO check for duplicates and fill in cached titles and artists
    # allow user modification
    user_video_info = user_modification(new_playlist_titles, logger) # refined playlist titles
    logger.info("User modification complete")


    video_objects = []
    youtube_web_driver = web_driver_utils.youtube_web_driver()
    for info in user_video_info:

        chosen_video_web_element = youtube_web_driver.find_official_song(info, logger)
        new_vdc = video_data_class(chosen_video_web_element, info, output_directory)

        video_objects.append(new_vdc)
    youtube_web_driver.close()



    # download video_objects
    youtube_dl_utils.download_all(video_objects, logger)

    # log metadata
    video_object :video_data_class
    for video_object in video_objects:
        video_object.log_meta_data(output_directory)
        video_object.attach_meta_data()



if __name__ == "__main__":
    main()

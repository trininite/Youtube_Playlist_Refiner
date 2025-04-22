import json

from os import path

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

#from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError, TIT2, TPE1, WOAS, WOAR, TXXX

class video_data_class:
    def __init__(self, ytd_video_renderer :WebElement, song_info :tuple, output_dir :str):

        self.ytd_video_renderer = ytd_video_renderer

        # assigns values from user input
        self.song_title, self.artist = song_info

        # assign all core info
        self.video_title, self.video_link, self.view_count = self.get_video_info()
        self.thumbnail_link = self.get_thumbnail()
        self.channel_name, self.channel_link = self.get_channel_info()

        # used for prompting user and searching for song
        self.complete_title = f"{self.song_title} - {self.artist}"

        # generate the file name based on the title
        self.file_name = f"{self.complete_title}.mp3".replace(" ", "_")
        
        # set output directory
        self.file_location = f"{output_dir}/{self.file_name}"

        # pre-define variables for post-download
        self.file_hex = None
        self.metadata = None



    def get_video_info(self):
        #find <a> element with id "video-title"
        video_title_anchor = self.ytd_video_renderer.find_element(By.CSS_SELECTOR, "a#video-title")
        video_link = video_title_anchor.get_attribute("href") #RETURNED

        # removes any extra options from the url
        if '&' in video_link:
            video_link = video_link.split('&')[0]

        yt_formatted_string = video_title_anchor.find_element(By.TAG_NAME, "yt-formatted-string")
        video_title = yt_formatted_string.get_attribute("innerHTML")

        aria_label = yt_formatted_string.get_attribute("aria-label")
        sections = aria_label.split(" ")

        # handles if view count isnt present, which it sometimes isnt  (for some reason)
        if "views" in sections:
            views_str_index = sections.index("views")
            view_count_index = views_str_index - 1 if views_str_index > 0 else None
        if view_count_index is None:
            self.view_count = 0
            return


        view_count = sections[view_count_index]

        return video_title, video_link, view_count


    def get_thumbnail(self):
        ytd_thumbnail = self.ytd_video_renderer.find_element(By.TAG_NAME, "ytd-thumbnail")
        yt_image = ytd_thumbnail.find_element(By.TAG_NAME, "yt-image")
        inner_image = yt_image.find_element(By.TAG_NAME, "img")

        thumbnail_link = inner_image.get_attribute("src")

        if thumbnail_link is None:
            thumbnail_link = "None"

        return thumbnail_link


    def get_channel_info(self):
        ytd_video_meta_block = self.ytd_video_renderer.find_element(By.TAG_NAME, "ytd-video-meta-block")
        yt_formatted_string = ytd_video_meta_block.find_element(By.TAG_NAME, "yt-formatted-string")
        channel_anchor = yt_formatted_string.find_element(By.TAG_NAME, "a")


        channel_link = channel_anchor.get_attribute("href")
        channel_name = channel_anchor.get_attribute("innerHTML")

        return channel_link, channel_name
    
    def print_info(self) -> None:
        """
        Print the video information and links.

        This function prints the video information and links. It includes the video title,
        channel name, and view count. It also includes the video link, channel link,
        and thumbnail link.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        print(f"Video Info:\n\
                    Video Title: {self.video_title}\n\
                    Channel Name: {self.channel_name}\n\
                    View Count: {self.view_count}\
                ")
        print(f"Links:\n\
                    Video Link: {self.video_link}\n\
                    Channel Link: {self.channel_link}\n\
                    Thumbnail Link: {self.thumbnail_link}\
                ")


    def gen_hex(self):
        self.file_hex :str = self.file_location.encode('utf-8').hex()


    def log_meta_data(self, output_directory : str) -> None:
        """
        Writes the metadata of a video to a JSON file.

        Args:
            video_object (video_data_class): An instance of the video_data_class
            containing the metadata of the video.

            output_directory (str): The directory where the JSON file will be saved.

        Returns:
            Dict
        """

        self.metadata = {
            "title": self.song_title,
            "artist": self.artist,
            "video_link": self.video_link,
            "thumbnail_link": self.thumbnail_link,
            "channel_name": self.channel_name,
            "channel_link": self.channel_link,
            "hex": self.file_hex
        }

        with open(f"{output_directory}/metadata.json", "w+", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=4)

    def attach_meta_data(self) -> None:
        assert path.exists(self.file_location), "mp3 failed to download"
        assert hasattr(self, "metadata"), "metadata uninitialized"

        try:
            audio = ID3(self.file_location)
        except ID3NoHeaderError as e:
            raise ID3NoHeaderError("mp3 failed to download") from e

        # tags
        TITLE = "TIT2"
        ARTIST = "TPE1"
        VIDEO_LINK = "WOAS"
        CHANNEL_LINK = "WOAR"
        CUSTOM = "TXXX"

        # standard tags
        audio[TITLE] = TIT2(encoding=3, text=self.metadata["title"])
        audio[ARTIST] = TPE1(encoding=3, text=self.metadata["artist"])
        audio[VIDEO_LINK] = WOAS(url=self.metadata["video_link"])
        audio[CHANNEL_LINK] = WOAR(url=self.metadata["channel_link"])

        # custom tags
        audio[CUSTOM] = TXXX(encoding=3, desc="hex", text=self.metadata["hex"])

        audio.save()
        
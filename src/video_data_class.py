from selenium import webdriver
from selenium.webdriver.common.by import By 
class video_data_class:
    def __init__(self, ytd_video_renderer, user_video_title, video_author):

        self.ytd_video_renderer = ytd_video_renderer

        video_info = self.get_video_info()
        assert video_info is not None
        self.video_title = video_info[0]
        self.video_link = video_info[1]
        self.view_count = video_info[2]

        thumbnail_info = self.get_thumbnail()
        assert thumbnail_info is not None
        self.thumbnail_link = thumbnail_info

        channel_info = self.get_channel_info()
        assert channel_info is not None
        self.channel_link = channel_info[0]
        self.channel_name = channel_info[1]

        self.user_video_title = user_video_title
        self.video_author = video_author
        self.complete_title = f"{self.user_video_title} - {self.video_author}"

        
        
        


        #TODO
        self.file_name = ""
        



    def get_video_info(self):
        #find <a> element with id "video-title"
        user_video_title_anchor = self.ytd_video_renderer.find_element(By.CSS_SELECTOR, "a#video-title")
        video_link = user_video_title_anchor.get_attribute("href")

        yt_formatted_string = user_video_title_anchor.find_element(By.TAG_NAME, "yt-formatted-string")
        user_video_title = yt_formatted_string.get_attribute("innerHTML")

        aria_label = yt_formatted_string.get_attribute("aria-label")
        sections = aria_label.split(" ")

        if "views" in sections:
            views_str_index = sections.index("views")
            view_count_index = views_str_index - 1 if views_str_index > 0 else None
        if view_count_index is None:
            raise Exception("view_count_index is less than 0")

        view_count = sections[view_count_index]       

        return(user_video_title, video_link, view_count)
        

    def get_thumbnail(self):
        ytd_thumbnail = self.ytd_video_renderer.find_element(By.TAG_NAME, "ytd-thumbnail")
        yt_image = ytd_thumbnail.find_element(By.TAG_NAME, "yt-image")
        inner_image = yt_image.find_element(By.TAG_NAME, "img")
        
        thumbnail_link = inner_image.get_attribute("src")
        
        if thumbnail_link is None:
            thumbnail_link = "None"



        return(thumbnail_link)


    def get_channel_info(self):
        ytd_video_meta_block = self.ytd_video_renderer.find_element(By.TAG_NAME, "ytd-video-meta-block")
        yt_formatted_string = ytd_video_meta_block.find_element(By.TAG_NAME, "yt-formatted-string")
        channel_anchor = yt_formatted_string.find_element(By.TAG_NAME, "a")


        channel_link = channel_anchor.get_attribute("href")
        channel_name = channel_anchor.get_attribute("innerHTML")
        
        return(channel_name, channel_link)
    
    def print_info(self):
        print(f"Video Info:\nVideo Title: {self.video_title}\nChannel Name: {self.channel_name}\nView Count: {self.view_count}\n")
        print(f"Links:\nVideo Link: {self.video_link}\nChannel Link: {self.channel_link}\nThumbnail Link: {self.thumbnail_link}")
    
    def gen_hex(self, output_dir :str):
        self.file_path = f"{output_dir}/{self.complete_title}.mp3"

        self.file_hex =self.file_path.encode('utf-8').hex()
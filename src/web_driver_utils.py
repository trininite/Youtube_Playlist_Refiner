#types
from logging import Logger
from selenium.webdriver.remote.webelement import WebElement

# webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class youtube_web_driver(webdriver.Firefox):
    def __init__(self):
        super().__init__()

    def find_official_song(self, song_info :tuple, logger :Logger) -> WebElement:

        base_search = "https://www.youtube.com/results?search_query="
        best_video_keyword = "%22topic%22"
        videos_only_keyword = "sp=EgIQAQ%253D%253D"
        search = f"{base_search}{song_info[0]} - {song_info[1]}+{best_video_keyword}&{videos_only_keyword}"

        self.get(search)

        #scroll down
        self.execute_script("window.scrollBy(0, 3500);")


        content = WebDriverWait(self, 10).until(
            EC.presence_of_element_located((By.ID, "contents"))
        )

        vids = content.find_elements(By.TAG_NAME, "ytd-video-renderer")

        result_count = len(vids)

        vid_choice = int(input(f"Enter a number between 0 and {result_count - 1}: "))

        while vid_choice < 0 or vid_choice >= result_count:
            input_message :str = f"Invalid input. Enter a number between 0 and {result_count - 1}: "
            vid_choice = int(input(input_message))


        return vids[vid_choice]

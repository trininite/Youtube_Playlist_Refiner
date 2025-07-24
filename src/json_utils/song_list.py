import json
from os import path, rename
import re
from rapidfuzz import fuzz

from .info_file import InfoFile

AUTO_ACCEPT = 95
REVIEW_MIN = 80

def clean_title(dirty_title:str):
    dirty_title= dirty_title.lower()
    dirty_title= re.sub(r'\(.*?\)|\[.*?]|official|video|lyrics|audio|hd|4k', '', dirty_title)
    dirty_title = re.sub(r'[^\w\s]', '', dirty_title, flags=re.UNICODE)
    dirty_title = re.sub(r'_', ' ', dirty_title)
    clean_title= re.sub(r'\s+', ' ', dirty_title).strip()
    return clean_title

class SongList(InfoFile):
    # json_file_path = path to the most recent song_list
    # song_info_list = list of song info read from json_file_path

    def __init__(self, mirror_path :str, action_time :str) -> None:
        super().__init__(mirror_path, action_time)

    def create_list(self, song_info_list :list[dict]) -> None:
        self.json_file_path = path.join(self.mirror_path, "song_list/INITIAL.json")

        if path.exists(self.json_file_path):
            raise Exception("Use of initial song list creation method when INITIAL.json already exists")


        self.song_info_list = song_info_list




    def read_list(self) -> None:
        self.json_file_path = path.join(self.mirror_path, "song_list/CURRENT.json")
        if not path.exists(self.json_file_path):
            self.json_file_path = path.join(self.mirror_path, "song_list/INITIAL.json")
        if not path.exists(self.json_file_path):
            raise Exception("No song_list found")

        with open(self.json_file_path, "r") as f:
            self.song_info_list = json.load(f)
        assert len(self.song_info_list) > 0, "song_info_list is empty"


        
    #TODO test adding new song to the playlist then
    def update_list(self, new_song_info_list: list[dict]) -> None:
        # map current songs by their ID for fast lookup
        current_songs_by_id = {
            song["url"].split("=")[-1]: song
            for song in self.song_info_list
        }
    
        seen_ids = set()
        updated_song_info_list: list[dict] = []
    
        for new_song in new_song_info_list:
            new_song_id = new_song["url"].split("=")[-1]
    
            if new_song_id in seen_ids:
                continue  # avoid duplicates if any
            
            if new_song_id in current_songs_by_id:
                updated_song_info_list.append(current_songs_by_id[new_song_id])
            else:
                updated_song_info_list.append(new_song)
    
            seen_ids.add(new_song_id)
    
        self.song_info_list = updated_song_info_list

    def save_list(self) -> None:
        self.json_file_path = path.join(self.mirror_path, "song_list/INITIAL.json")
        if path.exists(self.json_file_path):
            self.json_file_path = path.join(self.mirror_path, "song_list/CURRENT.json")
        if path.exists(self.json_file_path):
            rename(self.json_file_path, path.join(self.mirror_path, f"song_list/{self.action_time}.json"))

        with open(self.json_file_path, "w") as f:
            json.dump(self.song_info_list, f, indent=4, ensure_ascii=False)


    def run_duplicate_check(self):
        processed_indices: set[int] = set()

        for i, video_i in enumerate(self.song_info_list):
            if i in processed_indices:
                continue

            if video_i["duplicate"]:
                processed_indices.add(i)
                continue

            duplicates = []
            duplicate_indices = []

            video_i_title = clean_title(video_i["title"])

            for j, video_j in enumerate(self.song_info_list):
                if i == j or j in processed_indices:
                    continue

                if video_j["duplicate"]:
                    processed_indices.add(i)
                    continue

                video_j_title = clean_title(video_j["title"])
                ratio = fuzz.ratio(video_i_title, video_j_title)

                if ratio < REVIEW_MIN:
                    continue

                if ratio < AUTO_ACCEPT:
                    print(f"\nPossible duplicate:\n  {video_i_title}\n  {video_j_title}\n  Similarity: {ratio}%\n")
                    if input("Is this a duplicate? (y/n): ").strip().lower() != "y":
                        continue

                # found a duplicate
                if not duplicates:
                    duplicates.append(video_i["title"])
                    duplicate_indices.append(i)

                duplicates.append(video_j["title"])
                duplicate_indices.append(j)

            if duplicates:
                print("\nSelect the number of the title you want to KEEP:")
                for idx, title in enumerate(duplicates):
                    print(f"{idx}: {title}")
                while True:
                    try:
                        picked = int(input("> ").strip())
                        if 0 <= picked < len(duplicates):
                            break
                        else:
                            print("Invalid number. Try again.")
                    except ValueError:
                        print("Invalid input. Enter a number.")

                for idx, song_idx in enumerate(duplicate_indices):
                    if idx == picked:
                        continue
                    self.song_info_list[song_idx]["duplicate"] = True
                    processed_indices.add(song_idx)

            else:
                processed_indices.add(i)



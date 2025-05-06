#!usr/bin/env python3

# standard
from datetime import datetime

# custom
from dialogues import startup_dialogue
from dialogues import mirror_update_dialogue

from mirror_utils import create_mirror

#TODO move to SongList class
from mirror_utils import run_name_updater

from json_utils import MirrorInfo
from json_utils import SongList

from yt_utils import download_playlist_videos_info

#TODO move to SongList class
from yt_utils import run_dead_link_check

def main() -> None:
    action_time :str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_point :int = startup_dialogue()
    match start_point:
        # mirror creation, just creates the folder and mirror_info.json. 
        # also creates the INITIAL song list, doesn't look for duplicates
        
        case 1:
            mirror_path = create_mirror(action_time)


        # mirror update
        case 2:
            mirror_operation, mirror_path = mirror_update_dialogue()

            mirror_info = MirrorInfo(mirror_path, action_time)
            mirror_info.read_mirror_info()
            playlist_url = mirror_info.mirror_info_dict["url"]

            song_list :SongList = SongList(mirror_path, action_time)
            song_list.read_list()

            new_song_info_list :list[dict] = download_playlist_videos_info(playlist_url)
            song_list.update_list(new_song_info_list)
            

            match mirror_operation:
                # duplicate check
                case 1:
                    song_list.run_duplicate_check()
                    song_list.save_list()
                
                # dead link check
                case 2:
                    #song_list :list[dict] = read_song_list(mirror_path)
                    #updated_song_list :list[dict] = run_dead_link_check(song_list)
                    #generate_song_list(updated_song_list, mirror_path, action_time)
                    ...
                # name updater    
                case 3:
                    #song_list :list[dict] = read_song_list(mirror_path)
                    #updated_song_list :list[dict] = run_name_updater(song_list, mirror_path)
                    #generate_song_list(updated_song_list, mirror_path, action_time)
                    ...

            mirror_info.update_mirror_info()




if __name__ == "__main__":
    main()


# on this day, gta VI was delayed
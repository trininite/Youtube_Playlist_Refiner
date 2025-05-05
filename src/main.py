#!usr/bin/env python3

# standard
from datetime import datetime

# custom
from dialogues import startup_dialogue
from dialogues import mirror_update_dialogue

from mirror_utils import create_mirror
from mirror_utils import run_duplicate_check
from mirror_utils import run_name_updater

from json_utils import SongList
from json_utils.mirror_info import read_mirror_info


from yt_utils import run_dead_link_check

def main() -> None:
    action_time :str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_point :int = startup_dialogue()
    match start_point:
        # mirror creation, just creates the folder and mirror_info.json. 
        # also creates the INITIAL song list, doesn't look for duplicates
        
        case 1:
            create_mirror(action_time)

        # mirror update
        case 2:
            mirror_operation, mirror_path = mirror_update_dialogue()

            mirror_info = read_mirror_info(mirror_path)
            playlist_url = mirror_info["url"]
            playlist_info = download_playlist_info(playlist_url)
            generate_mirror_info(playlist_info, mirror_path, action_time)

            song_list :SongList = SongList(mirror_path, action_time)
            song_list.read_list()

            match mirror_operation:
                # duplicate check
                case 1:
                    song_list :list[dict] = read_song_list(mirror_path)
                    updated_song_list = run_duplicate_check(song_list)
                    generate_song_list(updated_song_list, mirror_path, action_time)
                
                # dead link check
                case 2:
                    song_list :list[dict] = read_song_list(mirror_path)
                    updated_song_list :list[dict] = run_dead_link_check(song_list)
                    generate_song_list(updated_song_list, mirror_path, action_time)

                # name updater    
                case 3:
                    song_list :list[dict] = read_song_list(mirror_path)
                    updated_song_list :list[dict] = run_name_updater(song_list, mirror_path)
                    generate_song_list(updated_song_list, mirror_path, action_time)
            



if __name__ == "__main__":
    main()


# on this day, gta VI was delayed
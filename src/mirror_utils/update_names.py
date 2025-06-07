from os import rename, path

def run_name_updater(song_list :list[dict], mirror_path :str) -> list[dict]:
    updated_song_list :list[dict] = []

    print("\
          This is for updating file names only. \
          Use '$CVT' to insert the current video title.\n\
          Use '$YCN' to insert the channel name.\n\
          To copy, use Ctrl + Shift + C\n\" \
          To paste, use Ctrl + Shift + V\n\
          Type nothing to leave as is.")

    for _, song in enumerate(song_list):
        print(f"\
            Youtube title: {song['title']}\n\
            Channel Name: {song['channel']}")

        new_file_name = input("Enter new title: ")   
        new_file_name = new_file_name.replace("$CVT", song['title'])
        new_file_name = new_file_name.replace("$YCN", song['channel'])      
        
        if new_file_name == "":
            updated_song_list.append(song)
            continue

        try:
            rename(path.join(mirror_path, song['file_name']), path.join(mirror_path, new_file_name))                
        except OSError as e:
            print(e)

            if not path.exists(mirror_path, song['file_name']):
                to_resource = True if input("[y/N]").upper() == "Y" else False
                if to_resource:
                    song["resource"] = True
                    updated_song_list.append(song)
                    continue
            print("File exists but cannot be renamed")

        song["file_name"] = new_file_name
        updated_song_list.append(song)

    return updated_song_list
import json
from datetime import datetime
from os import path, getcwd, geteuid

def mirror_info_json_generator(title :str, url :str, mirror_path :str, video_count :int) -> str:
    json_file_path = path.join(mirror_path, "mirror_info.json")
    
    print(json_file_path)

    if not path.exists(json_file_path):
        mirror_creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        mirror_info = {
            "title": title,
            "url": url,
            "video_count": video_count,
            "mirror_creation_time": mirror_creation_time,
            "mirror_last_updated": mirror_creation_time
        }

    print(mirror_info)
    # case for updating the info json file
    """elif path.exists(mirror_path):
        
        with open('mirror_info.json', 'r') as f:
            mirror_info = json.load(f)
            mirror_creation_time = datetime.strptime(mirror_info["mirror_creation_time"], "%Y-%m-%d %H:%M:%S")

            updated_mirror_info = {
                "title": title,
                "url": url,
                "video_count": video_count,
                "mirror_creation_time": mirror_creation_time,
                "last_updated": mirror_creation_time
            }
    """


        
    with open(json_file_path, 'w') as f:
        json.dump(mirror_info, f, indent=4)

    return json_file_path
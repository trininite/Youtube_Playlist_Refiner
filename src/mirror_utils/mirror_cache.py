#TODO change OS import to only include used functions
import os

def create_mirror_cache(mirror_path :str) -> None:
    ytpr_cache_dir :str = os.path.join(os.path.expanduser("~/.cache/"), "yt_playlist_refiner")
    os.makedirs(ytpr_cache_dir, exist_ok=True)


    if not os.path.exists(os.path.join(ytpr_cache_dir, "mirror_paths.txt")):
        with open(os.path.join(ytpr_cache_dir, "mirror_paths.txt"), "w") as f:
            f.write(mirror_path + "\n")
    else:
       with open(os.path.join(ytpr_cache_dir, "mirror_paths.txt"), "a") as f:
           f.write(mirror_path + "\n")

def cache_check():
    ytpr_cache_dir :str = os.path.join(os.path.expanduser("~/.cache/"), "yt_playlist_refiner")

    new_cache_list :list[str] = []
    removed_cache_list :list[str] = []

    with open(os.path.join(ytpr_cache_dir, "mirror_paths.txt"), "r") as f:
        mirror_paths = f.readlines()
    
    for mirror_path in mirror_paths:
        if os.path.exists(mirror_path.strip("\n")):
            new_cache_list.append(mirror_path)
            continue
    
        removed_cache_list.append(mirror_path)

    print("caches removed:")
    for removed_cache in removed_cache_list:
        print(removed_cache)

    os.remove(os.path.join(ytpr_cache_dir, "mirror_paths.txt"))
    with open(os.path.join(ytpr_cache_dir, "mirror_paths.txt"), "a") as f:
        for new_cache in new_cache_list:
            f.write(new_cache)


        
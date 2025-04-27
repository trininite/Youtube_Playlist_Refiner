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

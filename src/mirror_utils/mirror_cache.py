#TODO change OS import to only include used functions
import os

def create_mirror_cache(mirror_path :str) -> None:
    ytpr_cache_dir :str = os.path.join(os.path.expanduser("~/.cache/"), "yt_playlist_refiner")
    if not os.path.exists(ytpr_cache_dir):
        os.makedirs(ytpr_cache_dir, exist_ok=True)


    if not os.path.exists(os.path.join(ytpr_cache_dir, "mirror_paths.txt")):
        with open(os.path.join(ytpr_cache_dir, "mirror_paths.txt"), "w") as f:
            f.write(mirror_path + "\n")
    else:
       with open(os.path.join(ytpr_cache_dir, "mirror_paths.txt"), "a") as f:
           f.write(mirror_path + "\n")
           

def cache_check():
    ytpr_cache_dir = os.path.join(os.path.expanduser("~/.cache"), "yt_playlist_refiner")
    cache_file = os.path.join(ytpr_cache_dir, "mirror_paths.txt")

    working_cache_list = []
    removed_cache_list = []
    seen = set()

    # read and clean each path from file
    try:
        with open(cache_file, "r") as f:
            raw_paths = f.readlines()
    except FileNotFoundError:
        print("cache file not found.")
        return

    for raw_path in raw_paths:
        path = raw_path.strip().rstrip("/")  # remove newline + trailing slash

        if os.path.exists(path):
            # resolve and normalize path
            resolved = os.path.abspath(os.path.normpath(os.path.realpath(path)))

            if resolved not in seen:
                seen.add(resolved)
                working_cache_list.append(path)
            else:
                removed_cache_list.append(path)
        else:
            removed_cache_list.append(path)

    if removed_cache_list:
        print("caches removed:")
        for removed in removed_cache_list:
            print(removed)

        with open(cache_file, "w") as f:
            for path in working_cache_list:
                f.write(path + "\n")
    else:
        print("no caches removed")


        
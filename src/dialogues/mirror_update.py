import os


def mirror_update_dialogue() -> tuple[int, str]:
    cache_path :str = os.path.join(os.path.expanduser("~/.cache/"), "yt_playlist_refiner")
    with open(os.path.join(cache_path, "mirror_paths.txt"), "r") as f:
        mirror_paths = f.readlines()
    
    for i, mirror_path in enumerate(mirror_paths):
        print(f"{i}: {mirror_path}")

    mirror_index :int = int(input("Enter the number of the mirror you want to update: "))
    mirror_path = mirror_paths[mirror_index].strip("\n")
    
    mirror_name = mirror_path.split("/")[-1]


    print(f"{mirror_name} selected.")
    while True:
        print("\
            [1] Identify duplicates\n\
            [2] Identify dead links\n\
            [3] Download playlist\n")
        
        mirror_operation :int = int(input("Enter the number of the operation you want to perform: "))

        if mirror_operation > 3 or mirror_operation < 1:
            print("Invalid input, please try again.")
        else:
            break

    return mirror_operation, mirror_path




import clear_terminal
from time import sleep

def user_choice(video_data_objects, logger, choices):
    clear_terminal.clear_terminal()

    video_data_objects = video_data_objects[:choices]
    for i, vid in enumerate(video_data_objects):
        print(f"{i}:")
        vid.print_info()

    print(f"Enter a number between 0 and {choices}\nOr enter SKIP to skip this choice(WIP)")

    choice = int(input("\tChoice: "))

    if choice < 0:
        print("Invalid input")
        return(user_choice(video_data_objects, logger, choices))
    
    return(video_data_objects[choice])
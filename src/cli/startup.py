
def startup_dialogue():
    print("Welcome to the YouTube Playlist Refiner")
    start_point: int = input("If you're creating a new mirror, enter 1. If you're updating an existing mirror, enter 2: ")
    match start_point:
        case "1":
            return 1
        case "2":
            return 2
        case _:
            print("Invalid input, please try again.")
            return startup_dialogue()
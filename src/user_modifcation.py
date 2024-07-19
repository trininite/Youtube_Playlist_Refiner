import clear_terminal
from color_escape_codes import color

def confirm_user_choice(new_title, old_title):
    clear_terminal.clear_terminal()
    
    print(f"{color.RED}Are you sure you want to replace:{color.RESET}\n\t{old_title}\n{color.RED}with:{color.RESET}\n\t{new_title}\n")
    confirm_choice = input("(Y|n): ").capitalize()
    match confirm_choice:
        case "":
            return True
        case "Y":
            return True
        case "N":
            return False
        case _:
            return confirm_user_choice(new_title, old_title)

def get_user_title(old_title):
    clear_terminal.clear_terminal()
    print("Enter the prompted information based on the title below (type 'cur' for the title to copy the old title):")
    print(old_title)
    title = input("Title: ")
    artist = input("Artist: ")

    

    if title == "cur":
        title = old_title


    if title != "" and artist != "":
        title_info = (title, artist)

        new_title = f"{title} - {artist}"
        if confirm_user_choice(new_title, old_title) == True:
            return title_info
    else:
        return(get_user_title(old_title))


def user_modification(old_titles: list, logger):
    new_titles = []

    #TODO switch to for loop
    while len(old_titles) > 0:
        old_title = old_titles[0]
        title_info = get_user_title(old_title)
        

        new_titles.append(title_info)
        old_titles = old_titles[1:]
        logger.info(f"Changed {old_title} -> {title_info[0]} - {title_info[1]}")
        

    return(new_titles)
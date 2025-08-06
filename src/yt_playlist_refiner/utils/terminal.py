from os import system as os_system
from platform import system as platform_system

def clear_terminal():
    sys_OS = platform_system()
    match sys_OS:
        case "Linux":
            os_system("clear")
        case "Windows":
            os_system("cls")
        case "Mac":
            os_system("reboot")
            quit()
        case _:
            raise Exception("Invalid System Type")


class console_colors:
    """
    Class that contains all the escape codes for colored text in the console. Use a color then use RESET.
    """
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


import platform
import os

def clear_terminal():
    sys_OS = platform.system()
    match sys_OS:
        case "Linux":
            os.system("clear")
        case "Windows":
            os.system("cls")
        case "Mac":
            print("fuck you")
            os.system("reboot")
            quit()
        case _:
            raise Exception("Invalid System Type")
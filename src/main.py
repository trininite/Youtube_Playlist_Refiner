#!usr/bin/env python3

# standard
import datetime
from os import mkdir, chdir, path
#import json

# custom
from dialogues import startup_dialogue

from mirror_utils import create_mirror


def main() -> None:
    start_point :int = startup_dialogue()

    match start_point:
        # mirror creation, just creates the folder and mirror_info.json. 
        # also creates the INITIAL song list, doesn't look for duplicates
        case 1:
            create_mirror()

        # mirror update
        case 2:
            ...
        
            



if __name__ == "__main__":
    main()

import logging
import datetime
from os import path, mkdir

def create_logger(playlist_name):
    if not path.exists("./log/"):
        mkdir("./log/")

    time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    with open(f"log/{playlist_name}_{time}.log", "w+", encoding="utf-8") as f:
        f.close()


    # Configure the logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"log/{playlist_name}_{time}.log", encoding='utf-8'),
            #logging.StreamHandler()
    ])

    # Create a logger
    return logging.getLogger(__name__)

import logging
import datetime

def create_logger(playlist_name):
    from os import listdir
    #print(listdir())
    time = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

    with open(f"log/{playlist_name}_{time}.log", "w+") as f:
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



"""
    Logger for console and file
"""

import logging
import os
from config import LOG_DIRECTORY

def make_logger(name=None):
    '''
        return Logger for console and file
    '''
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()

    os.makedirs(LOG_DIRECTORY,exist_ok=True)
    file_handler = logging.FileHandler(filename=LOG_DIRECTORY+name+".log")

    console_formatter = logging.Formatter(fmt="%(message)s")
    file_formatter = logging.Formatter(fmt="[%(asctime)s] %(levelname)s - %(message)s")

    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    console_handler.setFormatter(console_formatter)
    file_handler.setFormatter(file_formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

import logging
import os
from settings import get_dirs, get_base_path

logging.basicConfig(
    filename='logs/status.log',
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def write_to_log(log_path, content):
    BASE_PATH = get_base_path()
    print(f"BASE PATH IS: {BASE_PATH}")
    DIRS = get_dirs(BASE_PATH)
    print(f"THE LIST OF DIRECTORIES: {DIRS}")
    logging.info(content)


def write_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)


def read_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content

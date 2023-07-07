import logging
import os
from settings import get_dirs, get_base_path

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


def write_to_log(log_path, content):
    BASE_PATH = get_base_path()
    print(BASE_PATH)
    DIRS = get_dirs(BASE_PATH)
    print(DIRS)
    with open(os.path.join(DIRS[2], log_path), 'w') as f:
        f.write(str(logging.info(content)))
    logging.info(content)


def write_to_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)


def read_from_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return content

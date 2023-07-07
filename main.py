import os

from utils import write_to_log, write_to_file, read_from_file
from settings import get_base_path, get_dirs

# BASE_PATH = get_base_path()
# print(BASE_PATH)
# DIRS = get_dirs(BASE_PATH)
# print(DIRS)
# print(os.getcwd())
write_to_log("log1.txt", "Hello")

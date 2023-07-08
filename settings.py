import os


def get_base_path():
    BASE_DIR = os.getcwd()
    return BASE_DIR


def get_dirs(base):
    DIRS = [os.path.join(base, "replica"), os.path.join(base, "source"), os.path.join(base, "logs")]
    return DIRS

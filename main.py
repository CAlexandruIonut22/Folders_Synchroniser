import os
import shutil
import time
from filecmp import dircmp

import schedule

from settings import get_base_path
from utils import *


def sync_folders(dircmp):
    if "source" not in os.listdir(dircmp.right):
        shutil.copytree(dircmp.left, os.path.join(dircmp.right, "source"))  # copy original folder
        write_to_log(f"Copied {dircmp.left} to the {dircmp.right} dir")

    src_only_list = src_only(dircmp)  # get list of items ONLY in the source folders
    print(src_only_list)
    # if len(src_only_list) >= 1 or len(unsynced_files(dcmp)) > 0:  # copy files and subdirs from left to right

    # NEED TO CHECK FOR SYNC BASED ON CONTENTS WHEN THEY ARE DIFFERENT!
    if len(src_only_list) >= 1:  # copy files and subdirs from left to right
        for i in src_only_list:
            # print(i)
            if os.path.isfile(os.path.join(dircmp.left, i)) and i not in os.listdir(dircmp.right):  # Copy files
                # print("FILE")
                shutil.copy2(dircmp.left + "/" + i, dircmp.right + "/" + i)
                write_to_log(f"Copied {i} to the {dircmp.right} dir")
            elif os.path.isdir(os.path.join(dircmp.left, i)) and i not in os.listdir(dircmp.right):  # Copy folders
                # print("FOLDER")
                shutil.copytree(os.path.join(dircmp.left, i), os.path.join(dircmp.right, i))
                write_to_log(f"Copied {os.path.join(dircmp.left, i)} to {dircmp.right} ")
    elif len(src_only_list) == 0:
        write_to_log("Folders are synced!")


class Folder:
    def __init__(self, name='', path=''):
        self.name = name
        self.abs_path = path
        self.files_list = os.listdir(self.abs_path)

    def write_to_file(self, file_path, content):
        with open(file_path, 'w') as f:
            f.write(content)

    def read_from_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return content


BASE_PATH = get_base_path()

srcFolder = Folder(name='source', path=os.path.join(BASE_PATH, 'source'))
src_path = srcFolder.abs_path
src_list = srcFolder.files_list
src_name = srcFolder.name

replicaFolder = Folder(name='replica', path=os.path.join(BASE_PATH, 'replica'))
repl_path = replicaFolder.abs_path
repl_list = replicaFolder.files_list
repl_name = replicaFolder.name

dcmp = dircmp(src_path, repl_path, ignore=None, hide=None)

# Main call
src_path = str(input("Path of the source folder: "))
repl_path = str(input("Path of the replica folder: "))
log_path = str(input("Path of the log folder: "))
sync_interval = str(input("Interval of sync: "))  # format input string to differentiate Seconds/Minutes/Hours/Days

# Scheduler
schedule.every(1).minute.do(lambda: sync_folders(dcmp))

while True:
    # Checks whether a scheduled task
    # is pending to run or not
    schedule.run_pending()
    time.sleep(4)
    # NEED TO CHECK FOR SYNC BASED ON CONTENTS WHEN THEY ARE DIFFERENT!

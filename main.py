import shutil
import time
from filecmp import dircmp

import schedule

from utils import *

BASE_PATH = os.getcwd()


def sync_folders(dircmp, log_path):
    if "source" not in os.listdir(dircmp.right):
        shutil.copytree(dircmp.left, os.path.join(dircmp.right, "source"))  # copy original folder
        write_to_log(f"Copied original {dircmp.left} to the {dircmp.right} dir", log_path)

    repl_only_list = dcmp.right_only
    src_only_list = dircmp.left_only  # get list of items ONLY in the source folders
    unsync_list = dircmp.diff_files

    if len(repl_only_list) > 1 and 'source' in repl_only_list:  # remove what is in replica and not in source

        for i in repl_only_list:
            if os.path.isfile(os.path.join(dircmp.right, i)):  # Copy files
                os.remove(os.path.join(dircmp.right, i))
                write_to_log(f"Removed {i} from the {dircmp.right} dir", log_path)
            elif os.path.isdir(os.path.join(dircmp.right, i)) and i != "source":  # Copy folders
                shutil.rmtree(os.path.join(dircmp.right, i), ignore_errors=True)
                write_to_log(f"Removed {os.path.join(dircmp.right, i)} from the {dircmp.right} ", log_path)

    if len(src_only_list) >= 1:  # copy files and subdirs from source to replica
        for i in src_only_list:
            if os.path.isfile(os.path.join(dircmp.left, i)):
                # Copy files
                shutil.copy(dircmp.left + "/" + i, dircmp.right + "/" + i)
                write_to_log(f"Copied {i} to the {dircmp.right} dir", log_path)
            elif os.path.isdir(os.path.join(dircmp.left, i)) and not os.path.exists(os.path.join(dircmp.right, i)):
                # Copy folders
                shutil.copytree(os.path.join(dircmp.left, i), os.path.join(dircmp.right, i))
                write_to_log(f"Copied {os.path.join(dircmp.left, i)} to {dircmp.right} ", log_path)

    if len(unsync_list) >= 1:
        for i in unsync_list:
            if os.path.isfile(os.path.join(dircmp.left, i)):
                # Copy files
                with open(dircmp.left + "/" + i, 'r') as f:
                    with open(dircmp.right + "/" + i, "w") as f1:
                        for line in f:
                            f1.write(line)
                # shutil.copy2(dircmp.left + "/" + i, dircmp.right + "/" + i)
                write_to_log(f"Updated {i} to the {dircmp.right} dir", log_path)
            elif os.path.isdir(os.path.join(dircmp.left, i)) and not os.path.exists(os.path.join(dircmp.right, i)):
                # Copy folders
                shutil.copytree(os.path.join(dircmp.left, i), os.path.join(dircmp.right, i))
                write_to_log(f"Updated {os.path.join(dircmp.left, i)} to {dircmp.right} ", log_path)

    if len(src_only_list) == 0 and len(unsync_list) == 0:
        write_to_log("Folders are synced!", log_path)


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


if __name__ == '__main__':
    src_path = str(input("Path of the source folder: "))
    repl_path = str(input("Path of the replica folder: "))
    log_path = str(input("Path of the log folder: "))
    sync_interval = str(input("Interval of sync: "))

    sync_interval = sync_interval.split(" ")
    sync_val = int(sync_interval[0])

    sync_name = sync_interval[1].lower()

    srcFolder = Folder(name='source', path=src_path)
    src_path = srcFolder.abs_path
    src_list = srcFolder.files_list
    src_name = srcFolder.name

    replicaFolder = Folder(name='replica', path=repl_path)
    repl_path = replicaFolder.abs_path
    repl_list = replicaFolder.files_list
    repl_name = replicaFolder.name

    dcmp = dircmp(src_path, repl_path, ignore=None, hide=None)

    if sync_name == "seconds":
        schedule.every(sync_val).seconds.do(sync_folders, dcmp, log_path)

    elif sync_name == "minutes":
        schedule.every(sync_val).minutes.do(sync_folders, dcmp, log_path)

    elif sync_name == "hours":
        schedule.every(sync_val).hours.do(sync_folders, dcmp, log_path)

    while True:
        schedule.run_pending()
        time.sleep(1)

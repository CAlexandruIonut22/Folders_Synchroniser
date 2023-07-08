import os
import shutil
from filecmp import dircmp

from settings import get_base_path
from utils import write_to_log


def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left,
                                                   dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


# def get_diff_list(src_list, repl_list, src_path, repl_path):
#     diff_list = []
#     for i in src_list:
#         if os.path.isdir(src_path) and os.path.isdir(repl_path) and i not in repl_list:  # one way checking
#             diff_list.append(i)
#     return diff_list


def unsynced_files(dcmp):
    return dcmp.diff_files  # files in both a and b but have different contents


def get_identical_list(dcmp):
    return dcmp.same_files  # files in both a and b that are identical


def src_only(dcmp):
    return dcmp.left_only  # files and subdirs only in a and not b


def get_common_dirs(dcmp):
    return dcmp.common_dirs


def sync_folders(dcmp):
    if "source" not in os.listdir(dcmp.right):
        shutil.copytree(dcmp.left, os.path.join(dcmp.right, "source"))  # copy original folder
    src_list = src_only(dcmp)
    # print(len(src_list))
    if len(src_list) > 1:
        # copy files and subdirs from left to right
        for i in src_list:
            shutil.copy2(dcmp.left + "/" + i, dcmp.right + "/" + i)
            print(f"Coppied: {i}")
    elif len(src_list) == 0:
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

# print(get_identical_list(dcmp=dcmp))
# print(unsynced_files(dcmp=dcmp))
# print(src_only(dcmp=dcmp))

sync_folders(dcmp=dcmp)

# print(get_diff_list(src_list, repl_list, src_path, repl_path))
# write_to_log("Hello")

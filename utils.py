import logging
from datetime import datetime


def write_to_log(content):
    logging.basicConfig(
        filename='logs/' + f'status_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}',
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S',
        filemode='w')
    # BASE_PATH = get_base_path()
    # print(f"BASE PATH IS: {BASE_PATH}")
    # DIRS = get_dirs(BASE_PATH)
    # print(f"THE LIST OF DIRECTORIES: {DIRS}")
    logging.info(content)


def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        print("diff_file %s found in %s and %s" % (name, dcmp.left,
                                                   dcmp.right))
    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)


def unsynced_files(dcmp):
    return dcmp.diff_files  # files in both a and b but have different contents


def get_identical_list(dcmp):
    return dcmp.same_files  # files in both a and b that are identical


def src_only(dcmp):
    # print(dcmp.left_only)
    return dcmp.left_only  # files and subdirs only in a and not b


def get_common_dirs(dcmp):
    return dcmp.common_dirs

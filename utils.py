import logging
import os
from datetime import datetime


def write_to_log(content, log_path):
    if not os.path.isdir(log_path):
        os.mkdir(log_path)

    mylogs = logging.getLogger(__name__)
    mylogs.setLevel(logging.INFO)

    # file logs
    file = logging.FileHandler(f'{log_path}/status_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}')
    file.setLevel(logging.INFO)
    fileformat = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    file.setFormatter(fileformat)

    # console logs
    stream = logging.StreamHandler()
    streamformat = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
    stream.setLevel(logging.INFO)
    stream.setFormatter(streamformat)
    # handlers for both
    mylogs.addHandler(file)
    mylogs.addHandler(stream)
    # start logging
    mylogs.info(content)


def check2copy_content(src_f_path, repl_f_path):
    with open(src_f_path, 'r') as f1:
        content1 = f1.read()
    with open(repl_f_path, 'r') as f2:
        content2 = f2.read()
    if content1 == content2:
        return True
    else:
        return False

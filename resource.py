import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def make_folder(path, del_if_exist=False):
    try:
        os.stat(path)
    except:
        print(path)
        os.makedirs(path)


def remove_folder(path):
    # check if folder exists
    # remove if exists
    import shutil
    if os.path.exists(path):
        shutil.rmtree(path)


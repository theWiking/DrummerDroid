import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
__version__ = '0.2'

def make_folder(path, del_if_exist=False):
    try:
        os.stat(path)
    except:
        print(path)
        os.makedirs(path)


def remove_folder(path):

    import shutil
    if os.path.exists(path):
        shutil.rmtree(path)


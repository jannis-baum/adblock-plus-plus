import os, shutil

from definitions import TEMP_DIR

def clear_temp_files():
    shutil.rmtree(TEMP_DIR)
    os.mkdirs(TEMP_DIR)


import os
import shutil

def clean(path, file_list=[]):
    if file_list:
        for f in file_list:
            os.remove(os.path.join(path, f))
    else:
        shutil.rmtree(path)
        os.mkdir(path)
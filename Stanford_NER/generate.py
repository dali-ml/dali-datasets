import random
import sys

from os import listdir
from os.path import isdir, isfile, join, dirname, realpath


# add data to path
DATA_DIR = dirname(dirname(realpath(__file__)))
sys.path.append(DATA_DIR)
from utils import print_progress, execute_bash

THIS_DATA_DIR = dirname(realpath(__file__))

# important
ZIP_URL = 'http://cs224d.stanford.edu/assignment2/assignment2.zip'
ZIP_LOCAL = join(THIS_DATA_DIR, 'assignment2.zip')
UNZIPPED_LOCAL = join(THIS_DATA_DIR, "assignment2")

def delete_paths(paths):
    for path in paths:
        execute_bash('rm -rf %s' % (path,))


if __name__ == '__main__':
    local_files = [join(THIS_DATA_DIR, f) for f in ['train.txt', 'test.txt', 'dev.txt']]
    delete_paths([ZIP_LOCAL, join(THIS_DATA_DIR, "trees")] + local_files)
    execute_bash('wget -O %s %s' % (ZIP_LOCAL, ZIP_URL))
    execute_bash('unzip %s -d %s' % (ZIP_LOCAL, UNZIPPED_LOCAL))
    execute_bash('mv %s %s' % (join(UNZIPPED_LOCAL, "data", "ner", "train"), join(THIS_DATA_DIR, "train.txt")))
    execute_bash('mv %s %s' % (join(UNZIPPED_LOCAL, "data", "ner", "test.masked"), join(THIS_DATA_DIR, "test.txt")))
    execute_bash('mv %s %s' % (join(UNZIPPED_LOCAL, "data", "ner", "dev"), join(THIS_DATA_DIR, "dev.txt")))
    delete_paths([ZIP_LOCAL, UNZIPPED_LOCAL])

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
TEXT_URL = 'https://raw.githubusercontent.com/aritter/twitter_nlp/master/data/annotated/ner.txt'
UNZIPPED_LOCAL = join(THIS_DATA_DIR, "train.txt")

def delete_paths(paths):
    for path in paths:
        execute_bash('rm -rf %s' % (path,))

if __name__ == '__main__':
    delete_paths([UNZIPPED_LOCAL])
    execute_bash('wget -O %s %s' % (TEXT_URL, UNZIPPED_LOCAL))

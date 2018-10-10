import random
import sys

from os import listdir
from os.path import isdir, isfile, join, dirname, realpath

from parser import parse

# add data to path
DATA_DIR = dirname(dirname(realpath(__file__)))
sys.path.append(DATA_DIR)
from utils import print_progress, execute_bash

THIS_DATA_DIR = dirname(realpath(__file__))

TRAIN_FILE = join(THIS_DATA_DIR, "mc_train.txt")
TEST_FILE = join(THIS_DATA_DIR, "mc_test.txt")

# important
ZIP_URL      = 'http://research.microsoft.com/en-us/um/redmond/projects/mctest/data/MCTest.zip'
ZIP_URL_TEST = 'http://research.microsoft.com/en-us/um/redmond/projects/mctest/data/MCTestAnswers.zip'
ZIP_LOCAL = join(THIS_DATA_DIR, 'MCTest.zip')
ZIP_TEST_LOCAL = join(THIS_DATA_DIR, 'MCTestAnswers.zip')

def delete_paths(paths):
    for path in paths:
        execute_bash('rm -rf %s' % (path,))

if __name__ == '__main__':
    delete_paths([ZIP_LOCAL, join(THIS_DATA_DIR, "MCTest"), join(THIS_DATA_DIR, '*.{tsv,ans}')])
    delete_paths([ZIP_LOCAL, join(THIS_DATA_DIR, "MCTestAnswers"), join(THIS_DATA_DIR, '*.{tsv,ans}')])
    execute_bash('wget -O %s %s' % (ZIP_LOCAL, ZIP_URL))
    execute_bash('unzip %s -d %s' % (ZIP_LOCAL, THIS_DATA_DIR))
    execute_bash('wget -O %s %s' % (ZIP_TEST_LOCAL, ZIP_URL_TEST))
    execute_bash('unzip %s -d %s' % (ZIP_TEST_LOCAL, THIS_DATA_DIR))
    execute_bash('mv %s %s' % (join(THIS_DATA_DIR, "MCTest*", "*.{tsv,ans}"), THIS_DATA_DIR))
    delete_paths([ZIP_LOCAL,ZIP_TEST_LOCAL, join(THIS_DATA_DIR, "MCTest*")])
    delete_paths([join(THIS_DATA_DIR, TRAIN_FILE), join(THIS_DATA_DIR, TEST_FILE)])
    parse(THIS_DATA_DIR, TRAIN_FILE, TEST_FILE)

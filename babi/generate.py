import random
import sys

from os import listdir
from os.path import isdir, isfile, join, dirname, realpath


# add data to path
DATA_DIR = dirname(dirname(realpath(__file__)))
sys.path.append(DATA_DIR)
from utils import print_progress, execute_bash, findfiles

THIS_DATA_DIR = dirname(realpath(__file__))

# important
TARBALL_URL = 'http://www.thespermwhale.com/jaseweston/babi/tasks_1-20_v1-2.tar.gz'
TARBALL_LOCAL = join(THIS_DATA_DIR, 'babi.tar.gz')
OUTPUT_DIR = join(THIS_DATA_DIR, 'tasks_1-20_v1-2')
NORMALIZED_OUTPUT_DIR = join(THIS_DATA_DIR, 'tasks')

def delete_paths(paths):
    for path in paths:
        execute_bash('rm -rf %s' % (path,))

def fix_babi_file(fname):
    with open(fname, "r") as f:
        all_file = f.read()

    with open(fname, "w") as f:
        for line in all_file.split('\n'):
            line = line.replace('\t', ' ')
            if '?' in line:
                no_and_question, rest = line.split('?')
                rest = rest.strip()
                rest = rest.split(' ')
                answer = rest[0].replace(',', ' ')
                rest = ' '.join(rest[1:])
                line = '%s ?\t%s\t%s' % (no_and_question.strip(),
                                           answer.strip()+ ' .',
                                           rest.strip())
            else:
                line = ' .'.join(line.split('.'))
            f.write(line + '\n')
        f.flush()

if __name__ == '__main__':
    delete_paths([TARBALL_LOCAL, OUTPUT_DIR])
    execute_bash('rm -rf %s' % (NORMALIZED_OUTPUT_DIR,))
    execute_bash('wget -O %s %s' % (TARBALL_LOCAL, TARBALL_URL))
    execute_bash('mkdir %s' % (OUTPUT_DIR,))
    execute_bash('tar -xz -f %s -C %s' % (TARBALL_LOCAL, THIS_DATA_DIR))
    execute_bash('mv %s %s' % (OUTPUT_DIR, NORMALIZED_OUTPUT_DIR))
    delete_paths([TARBALL_LOCAL,])

    for f in findfiles(NORMALIZED_OUTPUT_DIR, "qa*.txt"):
        print("Converting %s to common QA format..." % (f,))
        fix_babi_file(f)

import random
import sys

from os import listdir
from os.path import isdir, isfile, join, dirname, realpath
from xml_cleaner import to_raw_text_markupless

# add data to path
DATA_DIR = dirname(dirname(realpath(__file__)))
sys.path.append(DATA_DIR)
from utils import print_progress, execute_bash



# important
TARBALL = 'http://www.cs.cmu.edu/~ark/QA-data/data/Question_Answer_Dataset_v1.2.tar.gz'
TRAIN_FILE = 'wikianswer_train.txt'
VALIDATE_FILE = 'wikianswer_validate.txt'
VALIDATION_SIZE = 0.1

# not so important
DATASET_DIR = 'Question_Answer_Dataset'
DATASET_FILE = 'question_answer_pairs.txt'
MIN_ANSWER_LENGTH = 1

# Who does that?
WINDOWS_ENCODING = 'latin-1'

def cleanup():
    execute_bash('rm -rf wikianswer.tar.gz %s*' % (DATASET_DIR,))


if __name__ == '__main__':
    cleanup()

    execute_bash('wget -O wikianswer.tar.gz %s' % (TARBALL,))
    execute_bash('tar -xz -f wikianswer.tar.gz')
    execute_bash('mv Question_Answer_Dataset* %s' % (DATASET_DIR,))

    directories = [d for d in listdir(DATASET_DIR)
                   if isdir(join(DATASET_DIR, d)) and d.startswith('S')]

    assert len(directories) > 0

    num_nonascii = 0
    num_too_short = 0
    output_content = []
    for d in [join(DATASET_DIR, d) for d in directories]:
        dataset_file = join(d, DATASET_FILE)
        assert isfile(dataset_file)
        with open(dataset_file, newline='', encoding=WINDOWS_ENCODING) as f:
            first = True
            for line in f:
                if first:
                    first = False
                    continue
                try:
                    line.encode('ascii')
                except Exception:
                    # ignore windows encoding errors.
                    num_nonascii += 1
                    continue

                tokens = line.split('\t')
                question = tokens[1].strip()
                answer = tokens[2].strip()
                # ignore one word answers
                if len(answer.split(' ')) <= MIN_ANSWER_LENGTH or '<' in answer + question:
                    num_too_short += 1
                    continue

                output_content.append((question, answer))

    print("Generated %d question answer pairs" % (len(output_content) ))
    print("Skipped %d pairs because of answer shorter than %d words" % (num_too_short, MIN_ANSWER_LENGTH))
    print("Skipped %d because of encoding issues." % (num_nonascii,))

    num_valid = 0
    num_train = 0

    with open(VALIDATE_FILE, 'wt') as fvalid:
        with open(TRAIN_FILE, 'wt') as ftrain:

            for i, qa in enumerate(output_content):
                question, answer = qa
                print_progress(i, len(output_content))
                question_tokens = []
                answer_tokens = []
                for line in to_raw_text_markupless(question):
                    question_tokens.extend(line)
                for line in to_raw_text_markupless(answer):
                    answer_tokens.extend(line)

                output_line = '%s\t%s\n' % (' '.join(question_tokens), ' '.join(answer_tokens))
                if random.random() < VALIDATION_SIZE:
                    fvalid.write(output_line)
                    num_valid += 1
                else:
                    ftrain.write(output_line)
                    num_train += 1



    print("Saved %d pairs in %s" % (num_train, TRAIN_FILE))
    print("Saved %d pairs in %s" % (num_valid, VALIDATE_FILE))
    cleanup()

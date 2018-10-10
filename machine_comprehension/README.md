Data format
=========

This is format of mc_test.txt and mc_train.txt, raw files from the dataset are also available.
All text values are tokenized.

The file starts with a line containing number of sections. The descriptions of sections follow.

Each section is composed of line with name, line with information from mechanical turk,
line with section text (information used for question answering), line with number of
questions. The descriptions of questions follow.

Each question is described, by a line containing question text, line containing type of question
(one or multiple), line containing the number of answers, followed by the answers and finally
a line containing correct answer id (0-indexed).

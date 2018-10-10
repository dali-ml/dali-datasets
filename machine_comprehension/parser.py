import os

from xml_cleaner import to_raw_text_markupless

class Questions(object):
    """
    Small class for holding question objects
    from machine comprehension dataset.
    Holds `question`, and a list of `answers`
    as strings. Also has a `question_type` field
    to store whether question is single or
    multiple-choice.
    """
    __slots__ = ["question", "answers", "question_type", "answer"]
    @classmethod
    def build(cls, qs):
        qtype = None
        questions = []
        current_q = None
        current_answers = []
        for q in qs:
            if q.startswith("multiple: ") or q.startswith("one: "):
                if current_q is not None:
                    questions.append(cls(current_q, current_answers, qtype))
                    current_answers = []
                    current_q = None
                qtype, current_q = q.split(": ", 2)
            else:
                current_answers.append(q)

        if current_q is not None:
            questions.append(cls(current_q, current_answers, qtype))
        return questions

    def __init__(self, question, answers, question_type, answer=0):
        self.question      = question
        self.answer        = answer
        self.answers       = answers
        self.question_type = question_type


class Section(object):
    """
    Section object contains the reading `text`
    and a list of `questions` (see Question above).
    """
    def __init__(self, parsed_text):
        self.section_name, self.turk_info, self.text, *qs =  parsed_text.split("\t")
        self.questions = Questions.build(qs)
        self.text = self.text.replace(r"\newline", "\n")

    def add_answers(self, answers):
        for question, ans in zip(self.questions, answers):
            if ans == 'A':
                question.answer = 0
            elif ans == 'B':
                question.answer = 1
            elif ans == 'C':
                question.answer = 2
            elif ans == 'D':
                question.answer = 3
            else:
                raise ValueError("The answer can only be [A-D] (was %r)" % (ans))

def to_token_string(text):
    tokens = to_raw_text_markupless(text)
    tokens = [' '.join(sentence_tokens) for sentence_tokens in tokens]
    tokens = ' '.join(tokens)
    return tokens

def store_sections(file_name, sections):
    contents = []
    contents.append(len(sections))
    for section in sections:
        contents.append(section.section_name);
        contents.append(section.turk_info);
        contents.append(to_token_string(section.text))
        contents.append(len(section.questions))
        for question in section.questions:
            contents.append(to_token_string(question.question))
            contents.append(question.question_type)
            contents.append(len(question.answers))
            for answer in question.answers:
                contents.append(to_token_string(answer))
            contents.append(question.answer)
    with open(file_name, "wt") as f:
        f.write('\n'.join(map(str, contents)) + '\n')

def parse(data_path, training_file, test_file):
    ans_sets = []
    tsv_sets = []
    dataset_names = set()
    for path in os.listdir(data_path):
        if path.endswith(".ans") or path.endswith(".tsv"):
            path, extension = os.path.splitext(path)
            dataset_names.add(path)

    for name in dataset_names:
        answer_path = os.path.join(data_path, name + ".ans")
        question_path = os.path.join(data_path, name + ".tsv")
        ans_sets.extend(
            [ans.split("\t") for ans in open(answer_path, "rt").read().split("\n") if len(ans) > 0]
        )
        tsv_sets.extend([Section(sec) for sec in open(question_path, "rt").read().split("\n") if len(sec) > 0])

    for ans_set, section in zip(ans_sets, tsv_sets):
        section.add_answers(ans_set)

    test = []
    training = []
    for section in tsv_sets:
        if 'test' in section.section_name:
            test.append(section)
        else:
            training.append(section)

    store_sections(training_file, training)
    store_sections(test_file, test)


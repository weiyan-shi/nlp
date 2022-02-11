import cn2an
import re

paths = ['lower_letter_text.text', 'number_text.text', 'percent_text.text', 'scores_text.text', 'dot_text.text',
         'time_text.text', 'note_text.text', 'math_text.text', 'other_lang_text.text']


def include_num(text):
    disturb = re.search(r'[\d]+\++[\d]', text) or re.search(r'[\d]+\-+[\d]', text) or re.search(r'[\d]+\*+[\d]',
                                                                                                text) or re.search(
        r'[\d]+➗+[\d]', text) or re.search(r'[\d]+\.[\d]', text) or re.search(r'[\d]+\:[\d]', text) or re.search(
        r'[\d]+/[\d]', text) or re.search(r'[\d]+%', text)
    return re.search(r'\d', text) and (not disturb)


def include_lower_letter(text):
    return re.search(r'[a-z]', text)


def include_percent(text):
    return re.search(r'[\d]+%', text)


def include_score(text):
    return re.search(r'[\d.]+/[\d]+', text)


def include_dot(text):
    return re.search(r'[\d]+\.[\d]+', text)


def include_time(text):
    return re.search(r'[\d]+:[\d]+', text)


def include_note(text):
    return re.search(r'\(.*\)', text)


def include_other_lang(text):
    return re.search(r'[\uAC00-\uD7A3\u0800-\u4e00]', text[:-1])


def include_math(text):
    return (re.search(r'[\d]+\++[\d]', text) or re.search(r'[\d]+\-+[\d]', text) or re.search(r'[\d]+\*+[\d]',
                                                                                              text) or re.search(
        r'[\d]+➗+[\d]', text))


def process(text):
    for i in text:
        text = arab2cn(text)



def class_txt(input_path, output_path, func):
    with open(output_path, "w") as w_f:
        with open(input_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                key, text = line.split(" ", 1)
                if func(text) and (not (re.search(r'^aishell', text) or re.search(r'^haitian', text))):
                    w_f.write(line)


if __name__ == '__main__':
    test_input_path = './data/data_clean/test.text'
    input_path = './data/data_clean/NIO_500w.text'
    for path in paths:
        class_txt(input_path, "./data/data_process/" + path, include_num)

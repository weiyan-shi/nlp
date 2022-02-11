from string import punctuation
import cn2an
import numpy as np
from zhon.hanzi import punctuation as zh_punctuation
import os
import re


def merge(text):
    words = text.split(' ')
    new_text = ''
    for idx, word in enumerate(words):
        if re.search(r'[a-zA-z]+', word) and len(words) > 1:
            if idx == 0:
                new_text = new_text + word + ' '
            elif idx != 0 and idx == len(words) - 1:
                if re.search(r'[a-zA-z]+', words[idx - 1]):
                    new_text = new_text + word
                else:
                    new_text = new_text + ' ' + word
            else:
                if re.search(r'[a-zA-z]+', words[idx - 1]):
                    new_text = new_text + word + ' '
                else:
                    new_text = new_text + ' ' + word + ' '
        else:
            new_text += word
    return new_text


def recover(input_path, output_path):
    with open(output_path, "w") as w_f:
        with open(input_path, 'r') as f:
            lines = f.readlines()
            print(len(lines))
            for line in lines:
                text = merge(line)
                w_f.write(text)


def unique(input_path, output_path):
    with open(output_path, "w") as w_f:
        with open(input_path, 'r') as f:
            lines = f.readlines()
            lines = np.unique(lines)
            print(len(lines))
            w_f.writelines(lines)


if __name__ == '__main__':
    # recover('./seg/test.text', './seg/test_merge.text')
    recover('./seg/seg_text.text', './seg/merge.text')
    unique('./seg/merge.text', './seg/unique.text')

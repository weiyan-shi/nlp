import numpy as np

if __name__ == '__main__':
    words = []
    with open('./seg/test_result.text', "w") as w_f:
        with open('./seg/result.text', 'r') as f:
            lines = f.readlines()
            print(len(lines))
            for line in lines:
                letters = list(line[:-1])
                words.extend(letters)
        words = np.unique(words)
        cnt = 0
        for i, word in enumerate(words):
            if i % 50 == 0 and i != 0:
                w_f.write('\n')
            w_f.write(word + ' ')

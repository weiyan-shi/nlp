import os

with open('text', 'w', encoding='utf8') as w_f:
    with open('lab.txt', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            else:
                path, value = line.split(' ', 1)
                files, file = os.path.split(path)
                key = file[:-4]
                w_f.write(key + ' ' + value)

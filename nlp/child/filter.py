with open('text', 'w', encoding='utf8') as w_f:
    with open('text_child', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            if len(line) == 1:
                continue
            else:
                key, value = line.split(' ', 1)
                if value == '\n' or value == 'NULL\n':
                    continue
                else:
                    w_f.write(line)

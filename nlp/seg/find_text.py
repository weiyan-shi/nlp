keys = []

with open('/mnt/beegfs/home/asr/weiyan.shi/key') as f:
    lines = f.readlines()
    for line in lines:
        if len(line):
            keys.append(line[:-1])

with open('text_child', 'w', encoding='utf8') as w_f:
    with open('text', 'r', encoding='utf8') as f:
        lines = f.readlines()
        for line in lines:
            key, value = line.split(' ', 1)
            if key in keys:
                w_f.write(line)

from multiprocessing.pool import ThreadPool

dic = {}
w_f = open('text_child_new', 'w', encoding='utf8')
ww_f = open('res', 'w', encoding='utf8')

with open('text') as f:
    lines = f.readlines()
    for line in lines:
        if len(line):
            key, val = line.split(' ', 1)
            dic[key] = val


def find(line):
    if len(line):
        key, path = line.split(' ')
        if 'ASR_CN_ADULT_NIO_310_2021_NONE' in path:
            return
        if key in dic.keys():
            w_f.write(key + ' ' + dic[key])
        else:
            ww_f.write(line)


with open('/mnt/beegfs/home/asr/weiyan.shi/wav.scp', 'r', encoding='utf8') as f:
    lines = f.readlines()
    with ThreadPool(processes=10000) as pool:
        pool.map(find, lines)

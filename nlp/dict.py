dic = {}
with open('tokens.map', 'r', encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        arr = line.split(' ')
        dic[arr[0]] = arr[1]

with open('lexicon.new.txt', 'w') as w_f:
    with open('lexicon.txt', 'r') as r_f:
        lines = r_f.readlines()
        for line in lines:
            x = ''
            arr = line.split(' ')
            words = arr[0]
            x = x + words + ' '
            for word in words:
                if word in dic.keys():
                    x = x + dic[word] + ' '
                else:
                    x = x + dic['<unk>'] + ' '
            x = x[:-1]
            x += '\n'
            w_f.write(x)

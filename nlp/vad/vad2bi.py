with open('gmm_vad_2bi.res', 'w') as w_f:
    with open('gmm_vad.res', 'r') as f:
        lines = f.readlines()
        for line in lines:
            key, value = line.split(' ', 1)
            words = value[:-1].split(' ')
            str = ''
            for word in words:
                if word == 'SIL':
                    str += '0 '
                else:
                    str += '1 '
            str = str[:-1]
            str += '\n'
            w_f.write(key + ' ' + str)

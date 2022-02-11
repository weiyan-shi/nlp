files = []
files.append('TestSet_Call_Customer/TestSet_Call_Customer-english02.txt')
files.append('TestSet_Media_Customer/TestSet_Media_Customer-english03.txt')
files.append('TestSet_Other_Customer/TestSet_Other_Customer-english04.txt')
files.append('TestSet_DC_Customer/English01/english01.txt')
files.append('TestSet_DC_Customer/English02/english02.txt')
files.append('TestSet_Navi_Customer/english04_TestSet_Navi_Customer-english04')
files.append('TestSet_UserManual/TestSet_UserManual-English04.txt')
with open('text', 'a') as w_f:
    for file in files:
        with open(file, 'r') as f:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if i == 0 or i == 1:
                    continue
                else:
                    segments = line.split('#')
                    key = segments[1][:-4]
                    value = segments[4]
                    w_f.write(key + ' ' + value + '\n')

from string import punctuation
import cn2an
from zhon.hanzi import punctuation as zh_punctuation
import os
import re

dic = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九', '10': '十'}
paths = ['lower_letter_text.text', 'number_text.text', 'percent_text.text', 'scores_text.text', 'dot_text.text',
         'time_text.text', 'note_text.text', 'math_text.text', 'other_lang_text.text']


def arab2single(num):
    new_num = ''
    for i in num:
        new_num += dic[i]
    return new_num


def check_num(num, spec_1, spec_2, spec_3, spec_4):
    if spec_2 or spec_4:
        return arab2single(num)
    if spec_3:
        if len(num) > 5:
            return arab2single(num)
        elif len(num) <= 5:
            return cn2an.an2cn(num)
    if len(num) > 4:
        return arab2single(num)
    elif len(num) < 4:
        return cn2an.an2cn(num)
    elif len(num) == 4:
        if spec_1:
            return cn2an.an2cn(num)
        else:
            return arab2single(num)


def arab2cn(text):
    pattern = re.compile(r'\d+')
    spec_1 = re.search(r'路+|度+', text)  # 路牌时间角度类
    spec_2 = re.search(r'fm+|调频+|广播+|频道+|台+|兆赫+', text)  # 广播类
    spec_3 = re.search(r'加+|减+|乘+|除+', text)  # 加减乘除类
    spec_4 = re.search(r'尾号+|来电+|打+|号码+|电话+|换电站+|拨通+|接通+', text)  # 电话类
    nums = pattern.findall(text)
    for num in nums:
        text = text.replace(num, check_num(num, spec_1, spec_2, spec_3, spec_4))
    return text


def percent2cn(text):
    pattern = re.compile(r'\d+%')
    percents = pattern.findall(text)
    for percent in percents:
        num = percent[:-1]
        new_percent = '百分之' + cn2an.an2cn(num)
        text = text.replace(percent, new_percent)
    return text


def score2cn(text):
    pattern = re.compile(r'[\d]+/[\d]+')
    percents = pattern.findall(text)
    for percent in percents:
        tmp_percent = percent.replace('/', ' ')
        num1, num2 = tmp_percent.split(" ", 1)
        new_percent = cn2an.an2cn(num2) + '分之' + cn2an.an2cn(num1)
        text = text.replace(percent, new_percent)
    return text


def delete_cn_punctuation(text):
    re_punctuation = "[{}]+".format(zh_punctuation)
    text = re.sub(re_punctuation, " ", text)
    return text


def delete_en_punctuation(text):
    re_punctuation = "[{}]+".format(punctuation)
    text = re.sub(re_punctuation, " ", text)
    return text


def dot2cn(text):
    pattern = re.compile(r'[\d]+\.[\d]+')
    dots = pattern.findall(text)
    for dot in dots:
        new_dot = dot.replace('.', '点')
        text = text.replace(dot, new_dot)
    return text


def time2cn(text):
    pattern = re.compile(r'[\d]+:[\d]+')
    times = pattern.findall(text)
    for time_ in times:
        new_time_ = time_
        pattern = re.compile(r'\d+')
        nums = pattern.findall(time_)
        nums[0] = cn2an.an2cn(nums[0])
        nums[1] = cn2an.an2cn(nums[1])
        if re.search(r'[0-2]?[0-9]?:[0-5][0-9]', new_time_):
            new_time_ = nums[0] + '点' + nums[1]
        else:
            new_time_ = nums[0] + '比' + nums[1]
        text = text.replace(time_, new_time_)
    return text


def delete_note(text):
    pattern = re.compile(r'\(.*\)')
    notes = pattern.findall(text)
    for note in notes:
        text = text.replace(note, '')
    return text


def math2cn(text):
    text = text.replace('+', '加')
    if re.search(r'路+|到+|小区+', text):
        text = text.replace('-', '杠')
    else:
        text = text.replace('-', '减')
    text = text.replace('*', '乘')
    text = text.replace('➗', '除')
    return text


def delete_nbsp(text):
    return text.replace(' ', ' ')


def include_foreign(text):
    text = text.strip()
    text = text.replace(' ', '')
    return re.search(r'[^a-z\u4e00-\u9fa5]', text)


def include_gaosu(text):
    pattern = re.compile(r'g[\d]+')
    gaosus = pattern.findall(text)
    for gaosu in gaosus:
        pattern = re.compile(r'\d+')
        num = pattern.findall(gaosu)
        text = text.replace(num, arab2single(num))
    return text


def process(text):
    text = delete_note(text)  # 删除(xxx)注解
    text = str.lower(text)  # 大写转小写 A -> a
    text = percent2cn(text)  # 百分数 100% -> 100百分之
    text = dot2cn(text)  # 小数点 . -> 点
    text = time2cn(text)  # 时间 18:30 18点30
    text = math2cn(text)  # 数学 1+2 1加2
    text = score2cn(text)  # 分数 1/2 2分之1
    text = include_gaosu(text)  # 高速g20
    text = arab2cn(text)  # 数字变汉字 1分之2 -> 一分之二
    text = delete_cn_punctuation(text)  # 去除中文标点
    text = delete_en_punctuation(text)  # 去除英文标点
    text = delete_nbsp(text)  # 去掉nbsp
    return text


def test(input_path):
    for path in paths:
        with open('./data_class/' + path, "w") as w_f:
            with open('./data_process/' + path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, text = line.split(" ", 1)
                    if re.search(r'^aishell', text) or re.search(r'^haitian', text):
                        continue
                    new_text = process(text)
                    if not include_foreign(new_text):
                        w_f.write(key + ' ' + new_text)


def main(input_path):
    with open('seg/result.text', "w") as w_f:
        with open(input_path, 'r') as f:
            lines = f.readlines()
            print(len(lines))
            for line in lines:
                key, text = line.split(" ", 1)
                if re.search(r'^aishell', text) or re.search(r'^haitian', text):
                    continue
                new_text = process(text)
                if not include_foreign(new_text):
                    w_f.write(key + ' ' + new_text)


def mini_test():
    with open('./data/data_final/result_test.text', "w") as w_f:
        with open('./data/data_process/number_text.text', 'r') as f:
            lines = f.readlines()
            print(len(lines))
            for line in lines:
                key, text = line.split(" ", 1)
                if re.search(r'^aishell', text) or re.search(r'^haitian', text):
                    continue
                new_text = process(text)
                if not include_foreign(new_text):
                    w_f.write(key + ' ' + new_text)


if __name__ == '__main__':
    # input_path = input("请输入要进行数据清洗的文件路径")
    # choice = input("您是否想将输入文件分成包含不同类型标注错误的几个文件，并且分别清洗这几个文件，以方便您对照吗？\n y/n")
    # if choice == 'n':
    #     main(input_path)
    # else:
    #     test(input_path)

    input_path = 'seg/huandian_text.text'
    unique_main(input_path)

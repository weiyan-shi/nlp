from string import punctuation
import cn2an
from zhon.hanzi import punctuation as zh_punctuation
import os
import re
import argparse

parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--input_path', type=str, default=None)
parser.add_argument('--class_data', type=bool, default=False)
args = parser.parse_args()

dic = {'0': '零', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '七', '8': '八', '9': '九',
       '10': '十'}
paths = ['lower_letter_text.text', 'number_text.text', 'percent_text.text', 'scores_text.text', 'dot_text.text',
         'time_text.text', 'note_text.text', 'math_text.text']


class DataClassAndClean:  # 分类后清洗类，将数据按照各种标注错误分类
    methods = []  # 区分类别的方法名列表
    func_dict = {}  # (方法名-函数)字典

    def __init__(self, path):
        if not os.path.exists(os.getcwd() + '/after_class'):  # 创建分类后文件保存的文件夹
            os.mkdir(os.getcwd() + '/after_class')
        self.input_path = path  # 输入路径
        self.output_path = os.getcwd() + '/'  # 输出路径
        self.methods = [method for method in dir(self) if callable(getattr(self, method)) if  # 构建区分类别的方法名列表
                        not method.startswith('_')]  # 'private' methods start from _
        self.func_dict = {'include_num': self.include_num, 'include_lower_letter': self.include_lower_letter,
                          # 构造(方法名-函数)字典
                          'include_percent': self.include_percent, 'include_score': self.include_score,
                          'include_dot': self.include_dot, 'include_time': self.include_time,
                          'include_note': self.include_note, 'include_math': self.include_math}

    @staticmethod
    def include_num(text):  # 是否包含数字
        disturb = re.search(r'[\d]+\++[\d]', text) or re.search(r'[\d]+\-+[\d]', text) or re.search(r'[\d]+\*+[\d]',
                                                                                                    text) or re.search(
            r'[\d]+➗+[\d]', text) or re.search(r'[\d]+\.[\d]', text) or re.search(r'[\d]+\:[\d]', text) or re.search(
            r'[\d]+/[\d]', text) or re.search(r'[\d]+%', text)
        return re.search(r'\d', text) and (not disturb)

    @staticmethod
    def include_lower_letter(text):  # 是否包含小写字母
        return re.search(r'[a-z]', text)

    @staticmethod
    def include_percent(text):  # 是否包含百分号
        return re.search(r'[\d]+%', text)

    @staticmethod
    def include_score(text):  # 是否包含/号
        return re.search(r'[\d.]+/[\d]+', text)

    @staticmethod
    def include_dot(text):  # 是否包含.号
        return re.search(r'[\d]+\.[\d]+', text)

    @staticmethod
    def include_time(text):  # 是否包含:号
        return re.search(r'[\d]+:[\d]+', text)

    @staticmethod
    def include_note(text):  # 是否包含.号
        return re.search(r'\(.*\)', text)

    @staticmethod
    def include_math(text):  # 是否包含加减乘除
        return (re.search(r'[\d]+\++[\d]', text) or re.search(r'[\d]+\-+[\d]', text) or re.search(r'[\d]+\*+[\d]',
                                                                                                  text) or re.search(
            r'[\d]+➗+[\d]', text))

    def class_txt(self, filename, func):  # 文本分类函数
        with open(self.output_path + 'after_class/' + filename + '.text', "w") as w_f:  # 读取文件
            with open(self.input_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, text = line.split(" ", 1)  # 键值区分开
                    if func(text) and (
                            not (re.search(r'^aishell', text) or re.search(r'^haitian', text))):  # 去除脏数据并且符合当前的分类函数func
                        w_f.write(line)  # 写入文件
        p = DataClean(self.output_path + 'after_class/' + filename + '.text',
                      '/after_class_and_clean', '/' + filename + '_result.text')  # 创建清洗类
        p.main()  # 清洗文本

    def main(self):
        for method in self.methods:  # 按照不同的分类函数依次分类+清洗
            if re.search(r'include', method):
                self.class_txt(method, self.func_dict[method])


class DataClean:  # 清洗类
    def __init__(self, input_path, output_path='/after_clean', filename='/result.text'):  # 初始化
        if not os.path.exists(os.getcwd() + output_path):  # 创建输出路径
            os.mkdir(os.getcwd() + output_path)
        self.input_path = input_path  # 输入路径
        self.output_path = os.getcwd() + output_path + filename  # 输出路径

    @staticmethod
    def arab2single(num):  # 将阿拉伯数字转换为单字发音：123->一二三 与之相反的是连贯发音 123->一百二十三
        new_num = ''
        for i in num:
            new_num += dic[i]
        return new_num

    def check_num(self, num, spec_1, spec_2, spec_3,
                  spec_4):  # 转换数字 其中 spec_1:[路牌 时间 角度]类 spec_2:[广播类] spec_3:[算术类] spec_4:[电话类]
        if spec_2 or spec_4:  # 如果是广播或者电话，转成单字发音
            return self.arab2single(num)
        if spec_3:  # 如果是算数类
            if len(num) > 5:  # 万以上的数字 单字发音
                return self.arab2single(num)
            elif len(num) <= 5:  # 万以下的数子 连贯发音
                return cn2an.an2cn(num)
        if len(num) > 4:  # 如果长度大于4 单字发音
            return self.arab2single(num)
        elif len(num) < 4:  # 如果长度小于4 连贯发音
            return cn2an.an2cn(num)
        elif len(num) == 4:  # 如果长度等于4
            if spec_1:  # 如果是[路牌 时间 角度]类
                return cn2an.an2cn(num)  # 连贯发音
            else:
                return self.arab2single(num)  # 否则单字发音

    def arab2cn(self, text):  # 将阿拉伯数字转换为汉字
        pattern = re.compile(r'\d+')  # 正则匹配几种类别
        spec_1 = re.search(r'路+|度+', text)  # 路牌 时间 角度类
        spec_2 = re.search(r'fm+|调频+|广播+|频道+|台+|兆赫+', text)  # 广播类
        spec_3 = re.search(r'加+|减+|乘+|除+', text)  # 加减乘除 算术类
        spec_4 = re.search(r'尾号+|来电+|打+|号码+|电话+|换电站+|拨通+|接通+', text)  # 电话类
        nums = pattern.findall(text)
        for num in nums:
            text = text.replace(num, self.check_num(num, spec_1, spec_2, spec_3, spec_4))  # 转换
        return text

    @staticmethod
    def percent2cn(text):  # 百分数转汉字
        pattern = re.compile(r'\d+%')
        percents = pattern.findall(text)
        for percent in percents:
            num = percent[:-1]
            new_percent = '百分之' + cn2an.an2cn(num)
            text = text.replace(percent, new_percent)
        return text

    @staticmethod
    def score2cn(text):  # 分数换汉字
        pattern = re.compile(r'[\d]+/[\d]+')
        percents = pattern.findall(text)
        for percent in percents:
            tmp_percent = percent.replace('/', ' ')
            num1, num2 = tmp_percent.split(" ", 1)
            new_percent = cn2an.an2cn(num2) + '分之' + cn2an.an2cn(num1)
            text = text.replace(percent, new_percent)
        return text

    @staticmethod  # 删除中文标点
    def delete_cn_punctuation(text):
        re_punctuation = "[{}]+".format(zh_punctuation)
        text = re.sub(re_punctuation, " ", text)
        return text

    @staticmethod  # 删除英文标点
    def delete_en_punctuation(text):
        re_punctuation = "[{}]+".format(punctuation)
        text = re.sub(re_punctuation, " ", text)
        return text

    @staticmethod
    def dot2cn(text):  # 点转汉字
        pattern = re.compile(r'[\d]+\.[\d]+')
        dots = pattern.findall(text)
        for dot in dots:
            new_dot = dot.replace('.', '点')
            text = text.replace(dot, new_dot)
        return text

    @staticmethod
    def time2cn(text):  # 冒号转汉字
        pattern = re.compile(r'[\d]+:[\d]+')
        times = pattern.findall(text)
        for time_ in times:
            new_time_ = time_
            pattern = re.compile(r'\d+')
            nums = pattern.findall(time_)
            nums[0] = cn2an.an2cn(nums[0])
            nums[1] = cn2an.an2cn(nums[1])
            if re.search(r'[0-2]?[0-9]?:[0-5][0-9]', new_time_):  # 如果匹配的是时间，则替换成"点"
                new_time_ = nums[0] + '点' + nums[1]
            else:  # 否则转换为"比"
                new_time_ = nums[0] + '比' + nums[1]
            text = text.replace(time_, new_time_)
        return text

    @staticmethod
    def delete_note(text):  # 删除备注
        pattern = re.compile(r'\(.*?\)')
        notes = pattern.findall(text)
        notes.sort()
        for note in notes:
            text = text.replace(note, '')
        return text

    @staticmethod
    def math2cn(text):  # 处理算术类
        text = text.replace('+', '加')  # 匹配到'+' 翻译成'加'
        if re.search(r'路+|到+|小区+', text):  # 如果匹配到了"路 到 小区" 则-翻译成'杠'
            text = text.replace('-', '杠')
        else:
            text = text.replace('-', '减')  # 否则匹配成'-'
        text = text.replace('*', '乘')  # 匹配到'*' 翻译成'乘'
        text = text.replace('➗', '除')  # 匹配到'➗' 翻译成'除'
        return text

    @staticmethod
    def delete_nbsp(text):  # 去掉所有nbsp
        return text.replace(' ', ' ')

    @staticmethod
    def include_foreign(text):
        text = text.strip()
        text = text.replace(' ', '')  # 去掉含有他国语言的句子
        return re.search(r'[^a-z\u4e00-\u9fa5]', text)

    def process(self, text):
        text = self.delete_note(text)  # 删除(xxx)注解
        text = str.lower(text)  # 大写转小写 A -> a
        text = self.percent2cn(text)  # 百分数 100% -> 百分之100
        text = self.dot2cn(text)  # 小数点 . -> 点
        text = self.time2cn(text)  # 时间 18:30 18点30
        text = self.math2cn(text)  # 数学 1+2 1加2
        text = self.score2cn(text)  # 分数 1/2 2分之1
        text = self.arab2cn(text)  # 数字变汉字 1分之2 -> 一分之二
        text = self.delete_cn_punctuation(text)  # 去除中文标点
        text = self.delete_en_punctuation(text)  # 去除英文标点
        text = self.delete_nbsp(text)  # 去掉nbsp
        return text

    def main(self):
        with open(self.output_path, "w") as w_f:  # 读写数据并清洗
            with open(self.input_path, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    key, text = line.split(" ", 1)
                    print(key)
                    if re.search(r'^aishell', text) or re.search(r'^haitian', text):  # 去掉脏数据
                        continue
                    new_text = self.process(text)
                    if not self.include_foreign(new_text):
                        w_f.write(key + ' ' + new_text)


if __name__ == '__main__':
    # if not args.class_data:  # 输出文件保存在当前路径 /Users/weiyan.shi/nlp/after_class/include_note.text
    #     p1 = DataClean(args.input_path)
    #     p1.main()
    # else:
    #     p2 = DataClassAndClean(args.input_path)
    #     p2.main()
    p1 = DataClean('./child/text')
    p1.main()

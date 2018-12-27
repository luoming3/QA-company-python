# coding:utf-8

from __future__ import unicode_literals

import re
import codecs
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import jieba.posseg as psg
import jieba

QUARTER_DICT_PATH = "D:/HanLP/data/dictionary/custom/quarterDict.txt"

UTIL_CN_NUM = {
    '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4,
    '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4,
    '5': 5, '6': 6, '7': 7, '8': 8, '9': 9
}
UTIL_CN_UNIT = {'十': 10, '百': 100, '千': 1000, '万': 10000}


def pprint(obj):
    if isinstance(obj, list):
        list_result = "["
        for each in obj:
            list_result += (unicode(each) + ", ")
        return list_result + "]"
    elif isinstance(obj, dict):
        dict_result = "{"
        for key in obj:
            dict_result += (unicode(key) + ":" + unicode(obj[key])) + ", "
        return dict_result + "}"


def add_dictionary(dict_path):
    with codecs.open(dict_path, 'r', encoding='utf-8') as f:
        line_list = f.readlines()
        for line in line_list:
            jieba.add_word(line.strip(), freq=1024, tag='m')


def cn2dig(src):
    """
    从个位数开始计算求和直到结束（每个百千万单位前面必有数 ），结果跟最后单位作比较，大于最后单位则该值即为所求
    :param src: 三百四十二 二十一 十二 八
    :return: 342 21 12 8
    """
    if src == "":
        return None
    str_num = re.match("\d+", src)
    if str_num:
        return int(str_num.group())
    trans_result = 0
    unit = 1
    for item in src[::-1]:
        if item in UTIL_CN_UNIT.keys():
            unit = UTIL_CN_UNIT[item]
        elif item in UTIL_CN_NUM.keys():
            num = UTIL_CN_NUM[item]
            trans_result += num * unit
        else:
            return None
    if trans_result < unit:
        # 这里的判断是专门为了十一至十九的转化
        trans_result += unit
    return trans_result


def year2dig(year):
    """
    :param year: 2018 18 二零一八
    :return: int(2018)
    """
    res = ''
    for item in year:
        if item in UTIL_CN_NUM.keys():
            res = res + str(UTIL_CN_NUM[item])
        else:
            res = res + item
    year_num = re.match("\d+", res)    # 匹配出年份的具体数字
    if year_num:
        if len(year_num.group()) == 2:
            # 18 -> 2018
            return int(datetime.today().year / 100) * 100 + int(year_num.group(0))
        else:
            return int(year_num.group())
    else:
        return None


def quarter2dig(quarter_str):
    """
    :param quarter_str: 第一季度 第一季 一季度
    :return: 1 1 1
    """
    for each_word in quarter_str:
        if each_word in UTIL_CN_NUM:
            return UTIL_CN_NUM[each_word]


def dig2cn(parse_date_list, raw_date_list):
    result_date = []
    for i in range(len(raw_date_list)):
        quarter_num = re.search(r'第?([1-4一二三四])[季度]+', raw_date_list[i])
        format_date_pattern = r'(\d+)([-/])(\d+)([-/])(\d+)'
        if quarter_num:
            result_date.append(parse_date_list[i][0:4] + "年" + "第" + quarter_num.group(1) + "季度")
        elif re.search(r'[日号]', raw_date_list[i]):
            result_date.append(re.sub(format_date_pattern, r'\1年\3月\5日', parse_date_list[i]))
        elif re.search(r'[月]', raw_date_list[i]):
            result_date.append(re.sub(format_date_pattern, r'\1年\3月', parse_date_list[i]))
        else:
            result_date.append(re.sub(format_date_pattern, r'\1年', parse_date_list[i]))
    return result_date


def check_date_valid(check_word):
    # print "-" * 10 + "check_time_valid -> begin" + "-" * 10
    bare_num = re.match("\d+$", check_word)
    if check_word is None or len(check_word) == 0:
        return None
    if bare_num and len(check_word) != 4:
        # print "Tips '日期格式为: xxxx年xx月xx日 or xxxx-xx-xx or xxxx/xx/xx or xxxx年第x季度'"
        return None
    else:
        return check_word


class DateExtract(object):
    def __init__(self):
        add_dictionary(QUARTER_DICT_PATH)

    @staticmethod
    def parse_datetime(msg):
        """
        将日期变为格式化日期
        :param msg: 二零一八年十二月十八日
        :return: '2018-12-18'
        """
        if check_date_valid(msg) is None:
            return None
        # noinspection PyBroadException
        try:
            dt = parse(msg, fuzzy=False)
            print "parse之后的值：", dt

            # return dt.strftime('%Y-%m-%d')
            return dt.strftime('%Y-%m-%d')
        except Exception:
            quarter_dict = {1: "3-31", 2: "6-30", 3: "9-30", 4: "12-31"}
            # try:
            # case1: 无年月日词
            if not re.search(r"[-年月号日]", msg):
                year_quarter = re.match(r"([0-9零一二两三四五六七八九十]{2,4})?"
                                        r"(第?[1-4一二三四][季度]+)", msg)
                if not year_quarter:
                    # 无季度词
                    # print "Tips '日期格式为: xxxx年xx月xx日 or xxxx-xx-xx or xxxx/xx/xx or xxxx年第x季度'"
                    return None
                else:
                    quarter_num = quarter2dig(year_quarter.group(2))
                    if not year_quarter.group(1):
                        # 无具体年份有季度词
                        return datetime.today().strftime('%Y-') + quarter_dict[quarter_num]
                    else:
                        # 有具体年份有季度词
                        year_num = year2dig(year_quarter.group(1))
                        return datetime.today().replace(year_num).strftime("%Y-") + quarter_dict[quarter_num]

            # case2: 有年月日词
            date_feature = re.match(
                    r"([0-9零一二两三四五六七八九十]{2,4}[-年])?"
                    r"(第?[1-4一二三四][季度]+)?"
                    r"([0-9一二两三四五六七八九十]{1,2}[-月])?"
                    r"([0-9一二两三四五六七八九十]{1,3}[-号日]?)?", msg)
            # print "match结果：", m.group()

            if date_feature.group():
                res = {
                    "year": date_feature.group(1),
                    "quarter": date_feature.group(2),
                    "month": date_feature.group(3),
                    "day": date_feature.group(4),
                }
                params = {}     # 用来储存日期的数字部分

                if res["year"] and res["quarter"]:
                    return datetime.today().replace(year2dig(res["year"][:-1])).strftime("%Y-") + \
                           quarter_dict[quarter2dig(res["quarter"])]

                # 将中文转化为数字
                for name in res:
                    if res[name] is not None and len(res[name]) > 1:
                        # print "匹配出来的年月日-------->", name + ":" + res[name]
                        if name == 'year':
                            tmp = year2dig(res[name][:-1])
                        elif name == 'day':
                            if re.findall(r'[-日号]', res[name]):
                                tmp = cn2dig(res[name][:-1])
                            else:
                                tmp = cn2dig(res[name])
                        else:
                            tmp = cn2dig(res[name][:-1])
                        if tmp:
                            params[name] = int(tmp)

                # 如果只输入月日，则返回当前的年月日时间
                if (params.get("month", 0) and params.get("month", 0) > 12) or \
                   (params.get("day", 0) and params.get("day", 0) > 31):
                    return None
                target_date = datetime.today().replace(**params)
                return target_date.strftime('%Y-%m-%d')
            else:
                return None
            # except Exception as e:
            #     # print e.message

    def date_extract(self, text):
        """
        识别句子的日期，如果有多个日期则输出多个日期
        :param text:
        :return:
        """
        # replace_sentence = get_replace_sentence(text)
        # if replace_sentence:
        format_date_pattern = r'(\d+)([-/])(\d+)([-/])(\d+)'
        text = re.sub(format_date_pattern, r'\1年\3月\5日', text)
        # print text

        raw_date_list = []
        date_str = ''
        year_key = {'至今': 0, '今年': 0, '去年': -1, '前年': -2}
        day_key = {'至今': 0, '今天': 0, '昨天': -1, '前天': -2}
        for k, v in psg.cut(text):
            if k in year_key:
                if date_str != '':
                    raw_date_list.append(date_str)
                date_str = (datetime.today() + relativedelta(years=year_key.get(k, 0))).strftime('%Y年').decode('utf-8')
            elif k in day_key:
                if date_str != '':
                    raw_date_list.append(date_str)
                date_str = (datetime.today() + timedelta(days=day_key.get(k, 0))).strftime('%Y年%m月%d日').decode('utf-8')
            elif date_str != '':
                if v in ['m', 't']:
                    date_str = date_str + k
                else:
                    raw_date_list.append(date_str)
                    date_str = ''
            elif v in ['m', 't']:
                date_str = k
        if date_str != '':
            raw_date_list.append(date_str)

        # 把raw_date_list没用的词去掉
        format_date_list = []   # 格式化日期 2018-04-05
        for w in raw_date_list[:]:
            right_date = self.parse_datetime(w)
            if right_date:
                format_date_list.append(right_date)
            else:
                raw_date_list.remove(w)
        print "raw_date_list 的值：", pprint(raw_date_list)

        # 将时间词替换为时间标记词 “昱”
        if raw_date_list:
            for each_raw_date in raw_date_list:
                text = re.sub(each_raw_date, '昱', text)

        # 将数字日期转化为中文日期
        chinese_date_list = dig2cn(format_date_list, raw_date_list)

        return text, chinese_date_list


if __name__ == '__main__':
    de = DateExtract()
    # print (get_replace_sentence("2018-4-4和2017/3/4，多少和2018/3/2和2014-7-6"))
    # print (get_replace_sentence("2017年1月2日和2017-1-1"))

    # test_text = '2018年12月18日'
    # test_text = '现在是二零一八年十二月十八日的时间'
    # test_text = '今天和昨天'
    # test_text = '今年8月7日和去年8月七日'
    # test_text = '8月7日和去年8月七日'
    # test_text = '16年-18年第一季度某公司的营收是多少'
    # test_text = '2018-6-7某公司的营收是多少'
    # test_text = "18年十二月十八日的第10天的天气"
    # test_text = "2016年营收高于10亿的公司有哪些"

    while True:
        test_text = raw_input("输入日期: ").decode('utf-8')
        sub_sentence, date_list = de.date_extract(test_text)
        print "sub_sentence: ", sub_sentence
        print "识别结果 -->", pprint(date_list), "<-- 识别结果"

        # print "-" * 20 + "jieba分词" + "-" * 20
        # result_jieba = ''
        # for word, nature in psg.cut(test_text):
        #     result_jieba += ("/".join([word, nature]) + ',')
        # print result_jieba

    #     # for k, v in psg.cut(text):
    #     #     # print k, v

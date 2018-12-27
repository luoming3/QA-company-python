# coding:utf-8

from __future__ import unicode_literals

import re
import time
from pyhanlp import *
import codecs
import numpy as np
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from DateExtract import DateExtract

ROOT_PATH = "D:/HanLP/data/"
VOCABULARY_PATH = ROOT_PATH + "question/vocabulary.txt"
QUESTION_TYPE_PATH = ROOT_PATH + "question/question_classification.txt"

# 自定义公司字典路径
COMPANY_PATH = ROOT_PATH + "dictionary/custom/companyDict.txt"
# 自定义财务指标字典路径
FINANCIAL_PATH = ROOT_PATH + "dictionary/custom/financialDict.txt"
# 自定义时间字典路径
TIME_PATH = ROOT_PATH + "dictionary/custom/timeDict.txt"
# 自定义公司属性字典路径
PROPERTY_PATH = ROOT_PATH + "dictionary/custom/propertyDict.txt"
# 自定义quarter字典路径
QUARTER_PATH = ROOT_PATH + "dictionary/custom/quarterDict.txt"


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


def add_dict(dict_path, pos_fre):
    with codecs.open(dict_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            CustomDictionary.add(line.strip(), pos_fre)


def insert_dict(dict_path, pos_fre):
    with codecs.open(dict_path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            CustomDictionary.insert(line.strip(), pos_fre)


def load_vocabulary():
    """加载特征辞典"""
    vocabulary_dict = dict()
    with codecs.open(VOCABULARY_PATH, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line_list = line.strip().split(":")
            vocabulary_dict[line_list[1]] = int(line_list[0])
    return vocabulary_dict


def load_question_type():
    """加载问题模板，用字典装载"""
    type_dict = dict()
    with codecs.open(QUESTION_TYPE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line_list = line.strip("\r\n").split(":")
            type_dict[int(line_list[0])] = line_list[1]
    return type_dict


class ModelProcess(object):
    def __init__(self):
        self.question_path = ROOT_PATH + "question/company_question"

        # 加载公司字典
        insert_dict(COMPANY_PATH, "ntc 1024")
        # 加载财务指标字典
        insert_dict(FINANCIAL_PATH, "nz 1024")
        # 加载时间字典
        insert_dict(TIME_PATH, "t 1024")
        # 加载property字典
        insert_dict(PROPERTY_PATH, "ng 1024")
        # 加载quarter字典
        insert_dict(QUARTER_PATH, "mq 1024")

        self.abstract_dict = dict()
        self.type_dict = load_question_type()
        self.vocabulary = load_vocabulary()
        self.n_v = len(self.vocabulary)
        self.nb_model = self.get_classifier()

        self.de = DateExtract()

    def analysis_query(self, query_sentence):
        """
        识别问句模板，找到关键词进行查询
        :param query_sentence: 输入问句
        :return: model_index->问句模板索引, result_model_list->识别出的关键词,
                 ab_result->问句词性化结果, result_date_list->识别的日期.
        """

        print '-' * 10 + "日期识别" + '-' * 10
        replace_sentence, result_date_list = self.de.date_extract(query_sentence)
        print "result_date_list: ", pprint(result_date_list)

        print "-" * 10 + "开始分词" + "-" * 10
        ab_result = self.query_abstract(replace_sentence)
        print "句子词性化结果：" + ab_result

        # 模板识别
        model_index, str_pattern = self.query_classify(ab_result)
        print u"问句的模板为：", str_pattern

        # 最终结果
        final_result = self.query_replace(str_pattern)
        print u"识别出查询关键词：", final_result
        result_model_list = final_result.split(" ")
        return model_index, result_model_list, ab_result, result_date_list

    # 将关键词词性化是为了预测该问句的模板
    def query_abstract(self, query_sentence):
        segment = HanLP.newSegment().enableCustomDictionary(True)
        terms = segment.seg(query_sentence)     # ArrayList
        print terms
        print "-" * 10 + u"分词结束" + "-" * 10

        abstract_result = ""
        t_count = 0
        for term in terms:
            term_str = unicode(term)    # type(term) = Term
            term_word = unicode(term.word)
            if ('/ntc' in term_str) or ('/nt' in term_str):
                abstract_result += "ntc "
                self.abstract_dict["ntc"] = term_word
            elif "/m" in term_str:
                abstract_result += "m "
                self.abstract_dict["m"] = term_word
            elif "/nz" in term_str:
                abstract_result += "nz "
                self.abstract_dict["nz"] = term_word
            elif ("/t" in term_str) and (t_count == 0):
                t_count += 1
                abstract_result += "t "
                self.abstract_dict["t"] = term_word
            elif ("/t" in term_str) and (t_count == 1):
                abstract_result += "t1 "
                self.abstract_dict["t1"] = term_word
            elif "/ng" in term_str:
                abstract_result += "ng "
                self.abstract_dict["ng"] = term_word
            else:
                abstract_result += (term_word + " ")
        pprint(self.abstract_dict)
        return abstract_result

    def query_classify(self, abstr):
        raw_vec = self.sentence2vec(abstr)
        model_index = self.nb_model.predict(np.array(raw_vec).reshape(1, -1))[0]
        print "问题类型模板index为：" + unicode(model_index) + ":" + self.type_dict[model_index]
        return model_index, self.type_dict[model_index]

    # 将模板特征识别为可查询特征
    def query_replace(self, str_pattern):
        pattern_list = str_pattern.split(" ")
        # print pattern_list
        for each_word in pattern_list:
            abstr_value = self.abstract_dict.get(each_word)
            if abstr_value:
                sub_pat = unicode(each_word + " ")
                str_pattern = re.sub(sub_pat, abstr_value + " ", str_pattern)
        # 将抽象化字典清空，为下一次咨询做准备
        self.abstract_dict = dict()
        return str_pattern.rstrip(" ")

    def sentence2vec(self, sentence):
        segment = HanLP.newSegment()
        terms = segment.seg(sentence)  # ArrayList
        str_terms = ''
        for term in terms:
            str_terms += (term.word + ' ')

        vec = [0] * self.n_v
        for term in terms:
            term_word = unicode(term.word)
            if term_word in self.vocabulary:
                vec[self.vocabulary[term_word]] = 1
        return vec

    def get_classifier(self):
        """得到分类器"""
        x, y = self.load_question_file(self.question_path)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3)

        model = OneVsRestClassifier(SVC(C=0.6, kernel='rbf', gamma=0.2, class_weight='balanced'))
        clf = model.fit(x, y)
        count = 0
        for i in range(len(x)):
            if abs(clf.predict(x[i].reshape(1, -1)) - y[i])[0] != 0:
                count += 1
        print count / float(len(x))
        return clf

    def load_question_file(self, file_path):
        """加载问题集作为分类器的训练集"""
        train_list = []
        train_y = []
        question_file_list = os.listdir(unicode(file_path))
        for each_file in question_file_list:
            train_label = int(re.match(r'\d+', each_file).group())
            question_file = os.path.join(file_path, each_file)
            with codecs.open(question_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    train_list.append(self.sentence2vec(line.strip()))
                    train_y.append(train_label)
        return np.array(train_list), np.array(train_y)


if __name__ == '__main__':
    mp = ModelProcess()
    while True:
        text = raw_input("请输入句子：").decode('utf-8')
        # text = "2018年第1季度新潮能源的营收"

        t0 = time.clock()
        mp.analysis_query(text)
        print "所用时: ", time.clock() - t0

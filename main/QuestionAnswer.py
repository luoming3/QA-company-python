# coding:utf-8

from __future__ import unicode_literals

from ModelProcess import *
from SearchService import SearchService


class QuestionAnswer(object):
    def __init__(self):
        self.model_process = ModelProcess()

    def answer(self, question):
        model_index, result_model_list, ab_result, result_date_list = self.model_process.analysis_query(question)
        if model_index == 0:
            if SearchService.get_company_financial(result_model_list, ab_result, result_date_list):
                print "正确答案"
            else:
                print "未找到答案, 推荐"
        elif model_index == 1:
            if SearchService.get_financial_interval(result_model_list):
                print "正确答案"
            else:
                print "未找到答案"
        elif model_index == 2:
            if SearchService.search_answer(result_model_list):
                print "正确答案"
            else:
                print "未找到答案"
        elif model_index == 3:
            if SearchService.search_answer(result_model_list):
                print "正确答案"
            else:
                print "未找到答案"
        elif model_index == 4:
            if SearchService.search_answer(result_model_list):
                print "正确答案"
            else:
                print "未找到答案"
        elif model_index == 5:
            if SearchService.get_company_property(result_model_list, ab_result):
                print "正确答案"
            else:
                print "未找到答案"
        pprint(result_model_list)


if __name__ == '__main__':
    qa = QuestionAnswer()

    # process_test
    # while True:
    #     question_sentence = raw_input("请输入问题：\n退出请输入q\n").decode('utf-8')
    #     if question_sentence == 'q':
    #         break
    #     if len(question_sentence) > 0:
    #         questionService.answer(question_sentence)
    #     else:
    #         continue

    # precision_test
    question_list = ["18年第三季新潮能源的净利润是多少 0",
                     "18年-16年新潮能源的营收是多少 1",
                     "16年营收高于10亿的公司有哪些 2",
                     "16年营收低于10亿的公司有哪些 3",
                     "16年营收不低于10亿的公司有哪些 2",
                     "16年营收不少于10亿的公司有哪些 2",
                     "16年营收不多于10亿的公司有哪些 3",
                     "16年营收比10亿高的公司 2",
                     "16年营收比10亿大的公司 2",
                     "今年营收小于10亿的公司有哪些 3",
                     "今年营收排名前几的公司 4",
                     "18年新潮能源的业外支出是多少 0",
                     "16年新潮能源的投资收益 0",
                     "新潮能源行业分类 5",
                     "新潮能源电话是多少 5",
                     "新潮能源上市时间 5",
                     "17年营收排在前几的公司 4",
                     "17年营收处于前列的公司 4",
                     "13年营收名列前茅的公司有哪些 4",
                     "2015营收小于1千万的公司 3",
                     "今年的营收低于1000万的公司 3",
                     "2018营收比23亿多的公司 2",
                     "16年-2018年新潮能源的营收是 1",
                     "16年和2018年之间新潮能源的营收是 1",
                     "2015年新潮能源的营业成本 0",
                     "去年002909的营业额 0",
                     "002909在哪里 5",
                     "北京万通地产是否上市 5"]
    test_y = []
    question_sentence = []
    for each in question_list:
        question_sentence.append(each.split(" ")[0])
        test_y.append(int(each.split(" ")[1]))
    test_y = np.array(test_y)
    count2 = 0
    for i in range(len(question_sentence)):
        print '-' * 30
        y_predict, a, b, c = qa.model_process.analysis_query(question_sentence[i])
        result = abs(y_predict - test_y[i])
        if result != 0:
            count2 += 1
            print "WRONG"
        else:
            print "RIGHT"
    print "正确率：%.3f" % (100 - count2 / float(len(test_y)) * 100) + "%"

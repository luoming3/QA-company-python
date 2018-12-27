# coding:utf-8

from __future__ import unicode_literals

import re
import synonyms

PROPERTY_LIST = ["证券简称", "机构名称", "证券类别", "上市日期", "上市地点", "上市状态", "摘牌日期", "ISIN代码",
                 "英文名称", "英文简称", "成立日期", "注册资本", "法定代表人", "主营业务", "经营范围", "公司简介",
                 "省份", "城市", "注册地址", "办公地址", "邮编", "电话", "传真",
                 "邮件地址", "电子邮箱", "网站", "行业名称", "一级名称", "二级名称", "三级名称", "董事长", "独立董事",
                 "总经理", "董事会秘书", "董秘电话",
                 "董秘传真", "董秘邮箱", "证券事务代表", "会计师事务所", "律师事务所"]
FINANCIAL_LIST = ["合并类型编码", "合并类型", "营业收入", "营业成本", "营业税金及附加", "销售费用", "管理费用",
                  "财务费用", "资产减值损失", "投资收益",
                  "对联营企业和合营企业的投资收益", "营业利润", "营业外收入", "营业外支出", "非流动资产处置损失",
                  "利润总额", "所得税", "净利润",
                  "归属于母公司所有者的净利润", "少数股东损益", "基本每股收益", "营业总收入",
                  "营业总成本", "其他综合收益", "综合收益总额", "归属于母公司", "归属于少数股东", "非流动资产处置利得"]
QUARTER_DICT = {1: "3-31", 2: "6-30", 3: "9-30", 4: "12-31"}


def pprint(obj):
    if isinstance(obj, list):
        list_result = "["
        for each in obj:
            if isinstance(each, tuple):
                list_result += (pprint(each) + ", ")
            else:
                list_result += (unicode(each) + ", ")
        return list_result + "]"
    elif isinstance(obj, dict):
        dict_result = "{"
        for key in obj:
            dict_result += (unicode(key) + ":" + unicode(obj[key])) + ", "
        return dict_result + "}"
    elif isinstance(obj, tuple):
        tuple_result = "("
        for each in obj:
            tuple_result += (unicode(each) + ", ")
        return tuple_result + ")"


def similar_compute(ab_result, target_list):
    similar_result = []
    p_dict = dict()
    count = 0
    for each in target_list:
        p_value = synonyms.compare(ab_result, each)
        p_dict[count] = p_value
        count += 1
    for index, value in sorted(p_dict.items(), key=lambda x: x[1], reverse=True)[0:5]:
        similar_result.append((target_list[index], value))

    return similar_result


class SearchService(object):
    def __init__(self):
        pass

    @staticmethod
    def search_answer(model_list):
        answer = True
        for each in model_list:
            if re.search(r'ntc|nz|t|ng|mg|m', each):
                answer = False
                break
        return answer

    @staticmethod
    def get_company_financial(result_model_list, ab_result, result_date_list):
        answer = True
        for each in result_model_list:
            if re.search(r'ntc', each):
                print "该公司不存在"
                answer = False
            elif re.search(r'nz', each):
                print "公司该指标不存在，是否要找："
                print pprint(similar_compute(ab_result, FINANCIAL_LIST))
                answer = False
        if answer is True:
            if re.search(r'季度', result_date_list[0]):
                print result_date_list[0] + result_model_list[0] + "的" + result_model_list[2] + "是"
            else:
                print result_date_list[0] + "该年的四季dict"
        return answer

    @staticmethod
    def get_financial_interval(model_list):
        answer = True
        for each in model_list:
            if re.search(r'ntc|nz|t|ng|mg|m', each):
                answer = False
                break
        if answer:
            pass
        return answer

    @staticmethod
    def get_company_property(model_list, ab_result):
        answer = True
        for each in model_list:
            if re.search(r'ntc', each):
                print "该公司不存在"
                answer = False
            elif re.search(r'ng', each):
                print "公司该属性不存在，是否要找："
                print pprint(similar_compute(ab_result, PROPERTY_LIST))
                answer = False
        return answer

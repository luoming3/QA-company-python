# coding:utf-8

import re
import codecs
import pandas as pd


def pprint(obj):
    if isinstance(obj, list):
        list_result = "["
        for each in obj:
            list_result += (unicode(each) + ", ")
        print list_result + "]"
    elif isinstance(obj, dict):
        dict_result = "{"
        for key in obj:
            dict_result += (unicode(key) + ":" + unicode(obj[key])) + ", "
        print dict_result + "}"


filter_list = []
df = pd.read_csv("companyDict.txt", encoding='utf-8', header=None)
df_new = df.drop_duplicates(keep='first')
# with codecs.open("companyDict2.txt", 'w', encoding='utf-8') as f:
#     for each in list(df_new.iloc[:, 0].values):
#         f.write(each + '\n')
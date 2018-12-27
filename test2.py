# coding:utf-8

import jieba.posseg as psg
from datetime import datetime, timedelta

# 得到时间段内每一天的列表
date_list = []
begin_date = r'2018-7-8'
end_date = r'2018-8-7'
begin_date = datetime.strptime(begin_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")
while begin_date <= end_date:
    date_str = begin_date.strftime("%m-%d")
    date_list.append(date_str)
    begin_date += timedelta(days=1)
print date_list
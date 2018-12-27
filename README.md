# QA-company-python

## 配置环境

### pyhanlp

[配置pyhanlp](https://github.com/hankcs/pyhanlp/wiki/%E6%89%8B%E5%8A%A8%E9%85%8D%E7%BD%AE)
推荐半自动配置

### synonyms

pip install synonyms

## 流程图

![Image text](https://raw.githubusercontent.com/luoming3/picture_repository/master/process.jpg)

## main/主要文件

### DateExtract.py

可以识别文具中不规范日期, 例如 18年1季度 去年3月2日 2018-3-4 二零一八年五月一日 可以转化成如下格式化日期：
2018-3-31 2017-3-2 2018-3-4 2018-5-1 或者识别成中文格式化日期：2018年3月31日

### ModelProcess.py

加载自定义字典及识别问题模板的基本过程, 包括`分词`, `分类器训练`, `关键词词性化`, `识别问句模板`.

### SearchService.py

设置每个问题模板的回答, 并将提取的关键词进行查询.

### QuestionAnswer.py

测试文件.

## 其他文件

### gen_vocabulary.py

根据问题集生成one-hot-representation词库

### model_selection_gridsearchcv.py

网格搜索最佳模型及参数

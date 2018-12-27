# coding:utf-8

from __future__ import unicode_literals

from main.QuestionAnswer import *
# 问题集的分词应和用户输入的分词一致, 需要导入自定义词典
questionService = QuestionAnswer()


def gen_vocabulary():
    question_file = "D:/HanLP/data/question/company_question/"
    question_file_list = os.listdir(question_file)

    segment = HanLP.newSegment()
    vocabulary_dict = dict()
    count = 0

    for each_name in question_file_list:
        each_file = os.path.join(question_file, each_name)
        with codecs.open(each_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                terms = segment.seg(line.strip())
                print terms
                for term in terms:
                    if not re.findall('[ ,，]', term.word):
                        if vocabulary_dict.get(term.word) is not None:
                            continue
                        else:
                            print term.word, count
                            vocabulary_dict[term.word] = count
                            count += 1
    # pprint(vocabulary_dict)
    with codecs.open("vocabulary.txt", 'w', encoding='utf-8') as f:
        for value, index in sorted(vocabulary_dict.items(), key=lambda x: x[1], reverse=False):
            f.write(unicode(index) + ":" + value + "\n")


if __name__ == '__main__':
    gen_vocabulary()

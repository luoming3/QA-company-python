# coding:utf-8

from __future__ import unicode_literals

# from QuestionService import *
from pyhanlp import HanLP
import re
import numpy as np
from sklearn.metrics import roc_auc_score


if __name__ == "__main__":

    y_true = np.array([1, 0, 1, 0, 1, 0, 1])
    y_scores = np.array([0.8, 0.5, 0.7, 0.5, 0.5, 0.3, 0.5])
    print "y_true is ", y_true
    print "y_scores is ", y_scores
    print "AUC is", roc_auc_score(y_true, y_scores)

    # y_true = np.array([0, 1, 0, 1])
    # y_scores = np.array([0.1, 0.35, 0.4, 0.8])
    # print "y_true is ", y_true
    # print "y_scores is ", y_scores
    # print "AUC is ", roc_auc_score(y_true, y_scores)

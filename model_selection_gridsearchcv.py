# coding:utf-8

from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import make_scorer, accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.naive_bayes import BernoulliNB
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier

from main.ModelProcess import *
mp = ModelProcess()

data = load_breast_cancer()
x, y = mp.load_question_file(mp.question_path)


best_model_params = dict()
for i in range(5):
    # x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, random_state=0)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    k_fold = KFold(n_splits=5)
    scoring_fnc = make_scorer(accuracy_score)

    # SVM
    # model_SVM = OneVsRestClassifier(SVC(class_weight='balanced'))
    # params_SVM = {'estimator__C': np.arange(0.1, 1.5, 0.1),
    #               "estimator__kernel": ["linear", "rbf"],
    #               "estimator__gamma": np.arange(0.1, 1, 0.1)
    #               }
    #
    # grid_SVM = GridSearchCV(model_SVM, params_SVM, scoring_fnc, cv=k_fold)
    # grid_SVM = grid_SVM.fit(x_train, y_train)
    # reg_SVM = grid_SVM.best_estimator_
    #
    # print "-" * 10 + "result" + "-" * 10
    # print('best score: %f' % grid_SVM.best_score_)
    # final_params_dict = dict()
    # print('best parameters:')
    # for key in params_SVM.keys():
    #     final_params_dict[key] = reg_SVM.get_params()[key]
    #     print key, reg_SVM.get_params()[key]
    # print 'test score: %f' % reg_SVM.score(x_test, y_test)
    # best_model_params[reg_SVM.score(x_test, y_test)] = final_params_dict

    # RandomForest
    # model_RF = RandomForestClassifier()
    # params_RF = {'n_estimators': range(10, 110, 10),
    #              'max_depth': [5, 10, 15, 20, None],
    #              'min_samples_leaf': [1, 2, 3]}
    #
    # grid_RF = GridSearchCV(model_RF, params_RF, scoring_fnc, cv=k_fold)
    # grid_RF.fit(x_train, y_train)
    # reg_RF = grid_RF.best_estimator_
    #
    # print "-" * 10 + "result" + "-" * 10
    # print('best score: %f' % grid_RF.best_score_)
    # final_params_dict = dict()
    # print('best parameters:')
    # for key in params_RF.keys():
    #     final_params_dict[key] = reg_RF.get_params()[key]
    #     print key, reg_RF.get_params()[key]
    # print 'test score: %f' % reg_RF.score(x_test, y_test)
    # best_model_params[reg_RF.score(x_test, y_test)] = final_params_dict

    # NaiveBayes
    model_NB = OneVsRestClassifier(BernoulliNB())
    params_NB = {'estimator__alpha': np.arange(0, 2, 0.1)
                 }
    grid_NB = GridSearchCV(model_NB, params_NB, scoring_fnc, cv=k_fold)
    grid_NB = grid_NB.fit(x_train, y_train)
    reg_NB = grid_NB.best_estimator_

    print "-" * 10 + "result" + "-" * 10
    print('best score: %f' % grid_NB.best_score_)
    final_params_dict = dict()
    print('best parameters:')
    for key in params_NB.keys():
        final_params_dict[key] = reg_NB.get_params()[key]
        print key, reg_NB.get_params()[key]
    print 'test score: %f' % reg_NB.score(x_test, y_test)
    best_model_params[reg_NB.score(x_test, y_test)] = final_params_dict


print sorted(best_model_params.items(), key=lambda var: var[0], reverse=True)

# pd.DataFrame(grid.cv_results_).T

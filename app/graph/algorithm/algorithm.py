import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import SVC, SVR, LinearSVC, LinearSVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor


def training(data, func, params):
    params.pop('in2')
    cols = params.pop('label_columns')
    clf = func(**params)
    clf = clf.fit(data.drop(cols, axis=1), data[cols])
    return True, clf

def naive_bayes(in1, **params):
    return training(in1, GaussianNB, params)

def decision_tree(in1, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = DecisionTreeClassifier
    elif method == 'regress':
        func = DecisionTreeRegressor
    return training(in1, func, params)

def svm(in1, **params):
    method = params.pop('method', None)
    kernel = params.pop('kernel', 'linear')
    if kernel != 'linear':
        params['kernel'] = kernel
        if method == 'classify':
            func = SVC
        elif method == 'regress':
            func = SVR
    else:
        if method == 'classify':
            func = LinearSVC
        elif method == 'regress':
            func = LinearSVR
    return training(in1, func, params)

def knn(in1, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = KNeighborsClassifier
    elif method == 'regress':
        func = KNeighborsRegressor
    return training(in1, func, params)

def adaboost(in1, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = AdaBoostClassifier
    elif method == 'regress':
        func = AdaBoostRegressor
    return training(in1, func, params)

def neural_network(in1, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = MLPClassifier
    elif method == 'regress':
        func = MLPRegressor
    return training(in1, func, params)



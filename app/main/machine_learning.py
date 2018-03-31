import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.svm import NuSVC, NuSVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.ensemble import AdaBoostClassifier, AdaBoostRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor

def training(data, label, func, params):
    if len(data) != len(label):
        return False, None
    clf = func(**params)
    clf = clf.fit(data, label)
    return True, clf

def naive_bayes(in1, in2, **params):
    return training(in1, in2, GaussianNB, params)

def decision_tree(in1, in2, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = DecisionTreeClassifier
    elif method == 'regress':
        func = DecisionTreeRegressor
    return training(in1, in2, func, params)

def svm(in1, in2, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = NuSVC
    elif method == 'regress':
        func = NuSVR
    return training(in1, in2, func, params)

def knn(in1, in2, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = KNeighborsClassifier
    elif method == 'regress':
        func = KNeighborsRegressor
    return training(in1, in2, func, params)

def adaboost(in1, in2, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = AdaBoostClassifier
    elif method == 'regress':
        func = AdaBoostRegressor
    return training(in1, in2, func, params)

def neural_network(in1, in2, **params):
    method = params.pop('method', None)
    if method == 'classify':
        func = MLPClassifier
    elif method == 'regress':
        func = MLPRegressor
    return training(in1, in2, func, params)



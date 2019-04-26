import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier
__all__ = [
    'classify_adaboost',
    'classify_svm',
    'classify_neural_network',
    'classify_knn',
    'classify_naive_bayes',
    'classify_decision_tree',
]

def training(data, func, **kwargs):
    label = kwargs.pop('label')
    clf = func(**kwargs)
    clf = clf.fit(data.drop(label, axis=1), data[label])
    return clf

def classify_adaboost(data, **kwargs):
    params = {
        'label':kwargs.pop('label_columns'),
    }
    return training(data, AdaBoostClassifier, **params)

def classify_svm(data, **kwargs):
    params = {
        'kernel': kwargs.pop('kernel'),
        'label': kwargs.pop('label_columns'),
    }
    if params['kernel'] == 'linear':
        params.pop('kernel')
        return training(data, LinearSVC, **params)
    return training(data, SVC, **params)

def classify_neural_network(data, **kwargs):
    params = {
        'activation':kwargs.pop('activation'),
        'solver':kwargs.pop('solver'),
        'alpha':kwargs.pop('alpha'),
        'label':kwargs.pop('label_columns'),
    }
    return training(data, MLPClassifier, **params)

def classify_knn(data, **kwargs):
    params = {
        'label':kwargs.pop('label_columns')
    }
    return training(data, KNeighborsClassifier, **params)

def classify_naive_bayes(data, **kwargs):
    params = {
        'label':kwargs.pop('label_columns')
    }
    return training(data, GaussianNB, **params)

def classify_decision_tree(data, **kwargs):
    params = {
        'label':kwargs.pop('label_columns')
    }
    return training(data, DecisionTreeClassifier, **params)




import pandas as pd
from sklearn.ensemble import AdaBoostRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR, LinearSVR
from sklearn.tree import DecisionTreeRegressor
__all__ = [
    'regression_adaboost',
    'regression_svm',
    'regression_neural_network',
    'regression_knn',
    'regression_naive_bayes',
    'regression_decision_tree',
]

def training(data, func, **kwargs):
    label = kwargs.pop('label')
    clf = func(**kwargs)
    clf = clf.fit(data.drop(label, axis=1), data[label])
    return clf

def regression_adaboost(data, **kwargs):
    params = {
        'label':kwargs.pop('label_columns'),
    }
    return training(data, AdaBoostRegressor, **params)

def regression_svm(data, **kwargs):
    params = {
        'kernel': kwargs.pop('kernel'),
        'label': kwargs.pop('label_columns'),
    }
    if params['kernel'] == 'linear':
        params.pop('kernel')
        return training(data, LinearSVR, **params)
    return training(data, SVR, **params)

def regression_neural_network(data, **kwargs):
    params = {
        'activation':kwargs.pop('activation'),
        'solver':kwargs.pop('solver'),
        'alpha':kwargs.pop('alpha'),
        'label':kwargs.pop('label_columns'),
    }
    return training(data, MLPRegressor, **params)

def regression_knn(data, **kwargs):
    params = {
        'label':kwargs.pop('label_columns')
    }
    return training(data, KNeighborsRegressor, **params)

def regression_decision_tree(data, **kwargs):
    params = {
        'label':kwargs.pop('label_columns')
    }
    return training(data, DecisionTreeRegressor, **params)




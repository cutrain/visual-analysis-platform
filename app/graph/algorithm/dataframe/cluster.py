import pandas as pd
from sklearn.cluster import DBSCAN, KMeans
__all__ = [
    'dbscan',
    'kmeans',
]

def dbscan(data, **kwargs):
    eps = float(kwargs.pop('eps'))
    minpts = int(kwargs.pop('minpts'))
    predict_label = kwargs.pop('predict_labels')
    store = kwargs.pop('store_origin')
    clustering = DBSCAN(eps=eps, min_samples=minpts)
    df = pd.DataFrame(clustering.fit_predict(data))
    df.columns = [predict_label]
    if store == 'True':
        df = pd.concat([data, df], axis=1)
    return df

def kmeans(data, **kwargs):
    n_cluster = int(kwargs.pop('n_cluster'))
    max_iter = int(kwargs.pop('max_iter'))
    predict_label = kwargs.pop('predict_labels')
    store = kwargs.pop('store_origin')
    kmeans = KMeans(n_clusters=n_cluster, max_iter=max_iter)
    df = pd.DataFrame(kmeans.fit_predict(data))
    df.columns = [predict_label]
    if store == 'True':
        df = pd.concat([data, df], axis=1)
    return df

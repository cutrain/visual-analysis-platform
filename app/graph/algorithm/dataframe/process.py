import time
import pandas as pd
import numpy as np
from pandasql import sqldf

__all__ = [
    'random',
    'sql_execute',
    'sort',
    'dropna',
    'fillna',
    'drop_duplicate',
    'normalization',
    'merge_row',
    'merge_col',
    'split_row',
    'split_col',
]


def random(data, **kwargs):
    data = data.sample(frac=1, random_state=int(time.time())).reset_index(drop=True)
    return data

def sql_execute(data, **kwargs):
    command = kwargs.pop('sql_command')
    global df
    df = data
    command = command.format(this='df')
    pysqldf = lambda q: sqldf(q, globals())
    ret = pysqldf(command)
    return ret

def sort(data, **kwargs):
    cols = kwargs.pop('columns')
    ascending = kwargs.pop('ascending')
    na_position = kwargs.pop('na_position')
    cols = cols.split(',')
    ascending = True if ascending == 'True' else False
    data = data.sort_values(
        by=cols,
        ascending=ascending,
        kind='mergesort',
        na_position=na_position
    )
    return data

def dropna(data, **kwargs):
    t = kwargs.pop('drop_type')
    if t == "row":
        ret = data.dropna()
    if t == "col":
        ret = data.dropna(axis=1)
    if t == "all":
        ret = data.dropna(how="all")
    return ret

def fillna(data, **kwargs):
    t = kwargs.pop('fill_type')
    value = kwargs.pop('value')
    if t == "ffill":
        return data.fillna(method='ffill')
    if t == 'all':
        return data.fillna(value)
    if t == 'specific':
        value = value.split(',')
        args = {}
        for v in value:
            v = v.split(':')
            args.update({v[0]:v[1]})
        return data.fillna(args)
    raise NotImplementedError

def drop_duplicate(data, **kwargs):
    cols = kwargs.pop('columns')
    keep = kwargs.pop("keep")
    if cols == '':
        cols = None
    else:
        cols = cols.split(',')
    return data.drop_duplicates(subset=cols, keep=keep)

def normalization(data, **kwargs):
    method = kwargs.pop('method')
    cols = kwargs.pop('columns')
    if cols == '':
        cols = data.columns.tolist()
    else:
        cols = cols.split(',')
    ret = data.copy()
    tmp = []
    for i in range(len(cols)):
        if ret[cols[i]].dtype != np.dtype('O'):
            tmp.append(cols[i])
    cols = tmp

    if method == 'z-score':
        ret[cols] = (ret[cols] - ret[cols].mean())/ (ret[cols].std() + 1e-20)
    elif method == 'min-max':
        ret[cols] = (ret[cols] - ret[cols].min()) / (ret[cols].max() - ret[cols].min() + 1e-20)
    elif method == 'log':
        ret[cols] = np.log(ret[cols]) / np.log(ret[cols].max())
    elif method == 'atan':
        ret[cols] = np.arctan(ret[cols]) * 2. / np.pi
    else:
        raise NotImplementedError

    return ret

def merge_row(data1, data2, **kwargs):
    result = pd.concat([data1, data2])
    return result

def merge_col(data1, data2, **kwargs):
    how = kwargs.pop('how')
    if how == 'concat':
        result = pd.concat([data1, data2], axis=1)
    else:
        result = pd.merge(data1, data2, how=how)
    return result

def split_row(data, **kwargs):
    ratio = kwargs.pop('ratio')
    ratio = float(ratio)
    results = [0, 1]
    size = int(len(data) * (ratio / 100.))
    result1 = data[0:size]
    result2 = data[size:].reset_index(drop=True)
    return result1, result2

def split_col(data, **kwargs):
    cols = kwargs.pop('columns')
    cols = cols.split(',')
    result1 = data[cols]
    result2 = data.drop(cols, axis=1)
    return result1, result2


import time
import pandas as pd
import numpy as np

def random(in1, **params):
    df = in1
    df = df.sample(frac=1, random_state=int(time.time())).reset_index(drop=True)
    return True, df

def sql_execute(in1, **params):
    user = 'root'
    password = '123'
    host = 'localhost'
    port = '3306'
    database = 'temp'

    from sqlalchemy import create_engine
    con = create_engine(
        'mysql+mysqldb://' +
        user + ':' + password + '@' +
        host + ':' + port + '/' +
        database + '?charset=utf8')

    pd.io.sql.to_sql(in1, database, con=con, if_exists='replace')
    con.execute(params['sql_command'].format(this=database))
    df = pd.read_sql('select * from ' + database + ';', con)
    return True, df

def sort(in1, **params):
    params.pop('in2')
    cols = params.pop('columns').split(',')
    asc = True if params.pop('ascending') == "True" else False
    return True, in1.sort_values(by=cols, ascending=asc, kind='mergesort', **params)

def dropna(in1, **params):
    t = params.pop("drop_type")
    if t == "row":
        ret = in1.dropna()
    if t == "col":
        ret = in1.dropna(axis=1)
    if t == "all":
        ret = in1.dropna(how="all")
    return True, ret

def fillna(in1, **params):
    t = params.pop("fill_type")
    value = params.pop("value")
    if t == "ffill":
        return True, in1.fillna(method='ffill')
    if t == 'all':
        return True, in1.fillna(value)
    if t == 'specific':
        value = value.split(',')
        args = {}
        for v in value:
            v = v.split(':')
            args.update({v[0]:v[1]})
        return True, in1.fillna(args)

def drop_duplicate(in1, **params):
    keep = params.pop("keep", "first")
    if keep == 'None':
        keep = False
    cols = params.pop("columns", "").split(',')
    cnt = 0
    for col in cols:
        if len(col) == 0:
            cnt += 1
    if cnt == len(cols):
        cols = None
    a = pd.DataFrame([1,2,3])
    return True, in1.drop_duplicates(subset=cols, keep=keep)

def normalization(in1, **params):
    ret = in1.copy()
    method = params.pop("method", "z-score")
    cols = params.pop("columns", "").split(",")
    cnt = 0
    for col in cols:
        if len(col) == 0:
            cnt += 1
    if cnt == len(cols):
        cols = in1.columns.tolist()
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
        return False, "unknown normalization method"

    return True, ret



import os
import sqlite3
import pandas as pd

from tool import safepath
from config import DATA_DIR
from .graph.graphio import from_json_dicts, from_json_lists, from_mat_matrix, graph2json

__all__ = [
    'data_instream',
    'data_outstream',
    'sql_instream',
    'sql_outstream',
    'model_instream',
    'model_outstream',
    'image_instream',
    'image_outstream',
    'graph_instream',
    'graph_outstream',
]

def data_instream(**kwargs):
    num = int(kwargs.pop('read_number'))
    path = kwargs.pop('path')
    path = safepath(path)
    if num == 0:
        num = None
    df = pd.read_csv(os.path.join(DATA_DIR, path), nrows=num)
    return df

def data_outstream(data, **kwargs):
    path = kwargs.pop('path')
    path = safepath(path)
    data.to_csv(os.path.join(DATA_DIR, path), encoding='utf-8', index=False)

def sql_instream(**kwargs):
    dbtype = kwargs.pop('database_type')
    host = kwargs.pop('address')
    port = int(kwargs.pop('port'))
    user = kwargs.pop('user')
    passwd = kwargs.pop('password')
    dbname = kwargs.pop('database_name')
    num = int(kwargs.pop('read_number'))
    command = kwargs.pop('command')
    if dbtype == 'MySQL':
        import MySQLdb
        con = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=dbname
        )
    elif dbtype == 'sqlite':
        con = sqlite3.connect(os.path,join(dbname, DATA_DIR))
    elif dbtype == 'oracle':
        import cx_Oracle as cO
        con = cO.connect(
            user,
            passwd,
            host + ':' + str(port) + '/' + dbname
        )
    elif dbtype == 'SQLServer':
        import pymssql
        con = pymssql.connect(
            server=host,
            port=port,
            user=user,
            password=passwd,
            database=dbname
        )
    elif dbtype == "PostgreSQL":
        import psycopg2
        con = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=passswd,
            database=dbname,
        )

    data = pd.read_sql(command, con, nrows=num)
    con.close()
    return data

def sql_outstream(data, **kwargs):
    dbtype = kwargs.pop('database_type')
    host = kwargs.pop('address')
    port = int(kwargs.pop('port'))
    user = kwargs.pop('user')
    passwd = kwargs.pop('password')
    dbname = kwargs.pop('database_name')
    table_name = kwargs.pop('table_name')
    exist_method = kwargs.pop('if_exists')
    if dbtype == "MySQL":
        import MySQLdb
        con = MySQLdb.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=dbname
        )
    elif dbtype == 'sqlite':
        con = sqlite3.connect(os.path.join(DATA_DIR, dbname))
    elif dbtype == 'oracle':
        import cx_Oracle as cO
        con = cO.connect(
            user,
            passwd,
            host + ':' + str(port) + '/' + dbname,
        )
    elif dbtype == 'SQLServer':
        import pymssql
        con = pymssql.connect(
            server=host,
            port=port,
            user=user,
            password=passwd,
            database=dbname,
        )
    elif dbtype == "PostgreSQL":
        import psycopg2
        con = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=passwd,
            database=dbname,
        )

    data.to_sql(table_name, con, flavor='mysql', if_exists=exist_method)
    con.commit()
    con.close()

def model_instream(**kwargs):
    from sklearn.externals import joblib
    path = kwargs.pop('path')
    path = safepath(path)
    model = joblib.load(os.path,join(DATA, path))
    return model

def model_outstream(model, **kwargs):
    from sklearn.externals import joblib
    path = kwargs.pop('path')
    joblib.dump(model, os.path.join(DATA, path))

def image_instream(**kwargs):
    import cv2
    path = kwargs.pop('path')
    if type(path) == str:
        path = [path]
    images = []
    for i in path:
        images.append(cv2.imread(i))
    return images

def image_outstream(images, **kwargs):
    import cv2
    path = kwargs.pop('path')
    if len(imaegs) == 1:
        cv2.imwrite(os.path.join(DATA_DIR, path), images[0])
    else:
        cnt = 0
        realpath = os.path.join(DATA_DIR, path)
        if not os.path.exists(realpath):
            os.mkdir(realpath)
        for i in images:
            cv2.imwrite(os.path.join(realpath, str(cnt)+'.png'), i)
            cnt += 1

def graph_instream(**kwargs):
    path = kwargs.pop('path')
    path = safepath(path)
    graph = from_json_dicts(path)
    if graph is None:
        graph = from_json_lists(path)
    if graph is None:
        graph = from_mat_matrix(path)
    if graph is None:
        raise NotImplementedError
    return graph

def graph_outstream(graph, **kwargs):
    path = kwargs.pop('path')
    path = safepath(path)
    data = graph2json(graph)
    with open(os.path.join(DATA_DIR, path), 'wb') as f:
        f.write(data)


import pandas as pd
import sqlite3

from .error import err_wrap

def truepath(path, content=""):
    import os
    if os.path.isabs(path):
        return path
    return os.path.join(os.getcwd(), content, path)


@err_wrap
def data_instream(**params):
    num = int(params.pop('read_number', '0'))
    if num == 0:
        num = None
    df = pd.read_csv(truepath(params['path'], "data"), nrows=num)
    return True, df

@err_wrap
def sql_instream(**params):
    dbtype = params['database-type']
    if dbtype == 'MySQL':
        import MySQLdb
        con = MySQLdb.connect(
            host=params['address'],
            port=int(params['port']),
            user=params['user'],
            passwd=params['password'],
            db=params['database-name']
        )
    elif dbtype == 'sqlite':
        con = sqlite3.connect(truepath(params['database-name'], 'data'))
    elif dbtype == 'oracle':
        import cx_Oracle as cO
        con = cO.connect(
            params['user'],
            params['password'],
            params['address'] + '/' + params['host'] + ':' + int(params['port']) + '/' + params['database-name']
        )
    elif dbtype == 'SQLServer':
        import pymssql
        con = pymssql.connect(
            server=params['address'],
            port=int(params['port']),
            user=params['user'],
            password=params['password'],
            database=params['database-name']
        )
    elif dbtype == "PostgreSQL":
        import psycopg2
        con = psycopg2.connect(
            host=params['address'],
            port=int(params['port']),
            user=params['user'],
            password=params['password'],
            database=params['database-name']
        )

    df = pd.read_sql(params['command'], con)
    con.close()
    num = int(params.pop('read_number', '0'))
    if num != 0:
        df = df[:num]
    return True, df

@err_wrap
def model_instream(**params):
    from sklearn.externals import joblib
    model = joblib.load(truepath(params['path'], "model"))
    return True, model

@err_wrap
def data_outstream(in1, **params):
    df = in1
    df.to_csv(truepath(params['path'], "data"), encoding='utf-8', index=False)
    return True, None

@err_wrap
def sql_outstream(in1, **params):
    df = in1
    dbtype = params['database-type']
    if dbtype == "MySQL":
        import MySQLdb
        con = MySQLdb.connect(
            host=params['address'],
            port=int(params['port']),
            user=params['user'],
            passwd=params['password'],
            db=params['database-name']
        )
    elif dbtype == 'sqlite':
        con = sqlite3.connect(truepath(params['database-name'], 'data'))
    elif dbtype == 'oracle':
        import cx_Oracle as cO
        con = cO.connect(
            params['user'],
            params['password'],
            params['address'] + '/' + params['host'] + ':' + int(params['port']) + '/' + params['database-name']
        )
    elif dbtype == 'SQLServer':
        import pymssql
        con = pymssql.connect(
            server=params['address'],
            port=int(params['port']),
            user=params['user'],
            password=params['password'],
            database=params['database-name']
        )
    elif dbtype == "PostgreSQL":
        import psycopg2
        con = psycopg2.connect(
            host=params['address'],
            port=int(params['port']),
            user=params['user'],
            password=params['password'],
            database=params['database-name']
        )

    df.to_sql(params['table-name'], con, flavor='mysql', if_exists=params['if_exists'])
    con.commit()
    con.close()
    return True, None

@err_wrap
def model_outstream(in1, **params):
    model = in1
    from sklearn.externals import joblib
    joblib.dump(model, truepath(params['path'], "model"))
    return True, None



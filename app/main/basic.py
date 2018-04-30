import pandas as pd
import MySQLdb
from .error import err_wrap

def truepath(path, content=""):
    import os
    if os.path.isabs(path):
        return path
    return os.path.join(os.getcwd(), content, path)


@err_wrap
def data_instream(**params):
    return True, pd.read_csv(truepath(params['path'], "data"))

@err_wrap
def sql_instream(**params):
    con = MySQLdb.connect(
        host=params['address'],
        port=params['port'],
        user=params['user'],
        passwd=params['password'],
        db=params['database-name']
    )
    df = pd.read_sql('select * from ' + papram['table-name'] + ';', con)
    con.close()
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
    con = MySQLdb.connect(
        host=params['address'],
        port=params['port'],
        user=params['user'],
        passwd=params['password'],
        db=params['database-name']
    )
    df.to_sql(params['table-name'], con, flavor='mysql', if_exists='append')
    con.close()
    return True, None

@err_wrap
def model_outstream(in1, **params):
    model = in1
    from sklearn.externals import joblib
    joblib.dump(model, truepath(params['path'], "model"))
    return True, None



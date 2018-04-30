import pandas as pd
from .error import err_wrap

@err_wrap
def random(in1, **params):
    df = in1
    df = df.sample(frac=1)
    return True, df

@err_wrap
def sql_execute(in1, **params):
    con = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='temp'
    )
    in1.to_sql("temp", con, flavor='mysql', if_exists='replace')
    cursor = con.cursor()
    cursor.execute(params['sql_command'].format(this="temp"))
    con.commit()
    df = pd.read_sql('select * from temp;', con)
    con.close()
    return True, df

@err_wrap
def sort(in1, **params):
    params.pop('in2')
    cols = params.pop('columns').split(',')
    asc = True if params.pop('ascending') == "True" else False
    return True, in1.sort_values(by=cols, ascending=asc, kind='mergesort', **params)



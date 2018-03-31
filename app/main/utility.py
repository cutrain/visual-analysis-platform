import pandas as pd
from .error import err_wrap

@err_wrap
def predict(in1, in2, **params):
    model = in1
    data = in2
    df = pd.DataFrame(model.predict(data))
    print("in predict")
    print(df)
    return True, df

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



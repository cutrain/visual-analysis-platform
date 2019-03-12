import pandas as pd
from .error import err_wrap

@err_wrap
def predict(in1, in2, **params):
    model = in1
    data = in2
    cols = params.pop('label_columns', "").split(',')
    df = pd.DataFrame(model.predict(data.drop(cols, axis=1)))
    df.columns = params.pop('predict_labels', "predict_label").split(',')
    if params.pop('store_origin', 'False') == 'True':
        df = pd.concat([data, df], axis=1)
    return True, df

@err_wrap
def merge_row(in1, in2, **params):
    result = pd.concat([in1, in2])
    return True, result

@err_wrap
def merge_col(in1, in2, **params):
    how = params.pop('how', 'concat')
    if how == 'concat':
        result = pd.concat([in1, in2], axis=1)
    else:
        result = pd.merge(in1, in2, how=how, **params)
    return True, result

@err_wrap
def split_row(in1, **params):
    results = [0, 1]
    size = int(len(in1) * (float(params['ratio']) / 100.))
    results[0] = in1[0:size]
    results[1] = in1[size:].reset_index(drop=True)
    return True, results

@err_wrap
def split_col(in1, **params):
    results = [0, 1]
    cols = params['columns'].split(',')
    results[1] = in1[cols]
    results[0] = in1.drop(cols, axis=1)
    return True, results


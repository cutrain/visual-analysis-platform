import pandas as pd
from .error import err_wrap

@err_wrap
def random(in1, **params):
    df = in1
    df = df.sample(frac=1)
    return True, df

@err_wrap
def merge_row(in1, in2, **params):
    result = pd.concat([in1, in2])
    return True, result

@err_wrap
def merge_col(in1, in2, **params):
    result = pd.concat([in1, in2], axis=1)
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
    cols = params['cols'].split(',')
    results[1] = in1[cols]
    results[0] = in1.drop(cols, axis=1)
    return True, results




import pandas as pd
__all__ = [
    'predict',
]

def predict(skmodel, data, **kwargs):
    label = kwargs.pop('label_columns').split(',')
    predict_label = kwargs.pop('predict_labels')
    df = pd.DataFrame(skmodel.predict(data.drop(label, axis=1)))
    df.columns = [predict_label]
    if kwargs.pop('store_origin', 'False') == 'True':
        df = pd.concat([data, df], axis=1)
    return df

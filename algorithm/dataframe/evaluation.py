import pandas as pd
__all__ = [
    'fone',
    'recall',
    'accuracy',
]

def regular_data(data):
    data = data.astype(str)
    data = data.reset_index(drop=True)
    return data


def fone(data1, data2, **kwargs):
    from sklearn.metrics import f1_score
    true_posi = kwargs.pop('true_posi')
    avg = kwargs.pop('average')
    true_col = kwargs.pop('truth_column')
    pred_col = kwargs.pop('pred_column')
    if true_posi == 'right':
        temp = data1
        data1 = data2
        data2 = temp
    if true_col in data1.columns:
        true_data = data1[true_col]
    else:
        true_data = data1[data1.columns[0]]
    if pred_col in data2.columns:
        pred_data = data2[pred_col]
    else:
        pred_data = data2[data2.columns[0]]

    true_data = regular_data(true_data)
    pred_data = regular_data(pred_data)
    result = f1_score(true_data, pred_data, average=avg)
    result = pd.DataFrame([result], columns=['F1'])
    return result



def recall(data1, data2, **kwargs):
    from sklearn.metrics import recall_score
    true_posi = kwargs.pop('true_posi')
    avg = kwargs.pop('average')
    true_col = kwargs.pop('truth_column')
    pred_col = kwargs.pop('pred_column')
    if true_posi == 'right':
        temp = data1
        data1 = data2
        data2 = temp
    if true_col in data1.columns:
        true_data = data1[true_col]
    else:
        true_data = data1[data1.columns[0]]
    if pred_col in data2.columns:
        pred_data = data2[pred_col]
    else:
        pred_data = data2[data2.columns[0]]
    true_data = regular_data(true_data)
    pred_data = regular_data(pred_data)
    result = recall_score(true_data, pred_data, average=avg)
    result = pd.DataFrame([result], columns=['Recall'])
    return result


def accuracy(data1, data2, **kwargs):
    from sklearn.metrics import accuracy_score
    true_posi = kwargs.pop('true_posi')
    true_col = kwargs.pop('truth_column')
    pred_col = kwargs.pop('pred_column')
    if true_posi == 'right':
        temp = data1
        data1 = data2
        data2 = temp
    if true_col in data1.columns:
        true_data = data1[true_col]
    else:
        true_data = data1[data1.columns[0]]
    if pred_col in data2.columns:
        pred_data = data2[pred_col]
    else:
        pred_data = data2[data2.columns[0]]
    true_data = regular_data(true_data)
    pred_data = regular_data(pred_data)
    result = accuracy_score(true_data, pred_data)
    result = pd.DataFrame([result], columns=['Accuracy'])
    return result

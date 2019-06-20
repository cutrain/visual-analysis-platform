__all__ = [
    'outlier_iforest',
]

def outlier_iforest(data, **kwargs):
    import pandas as pd
    from pyod.models.iforest import IForest
    contamination = float(kwargs.pop('contamination'))
    clf = IForest(contamination=contamination)
    clf.fit(data)
    pred = clf.labels_
    df = pd.DataFrame(pred, columns=['is_outlier'])
    ret = pd.concat([data, df], axis=1)
    print('-'*100, flush=True)
    print(ret)

    print('-'*100, flush=True)
    return ret



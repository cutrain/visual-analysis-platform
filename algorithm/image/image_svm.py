__all__ = [
    'image_svm',
    'image_svm_apply',
]

def images2df(images):
    import numpy as np
    import pandas as pd
    data = np.stack(images)
    data = data.reshape(len(data),-1)
    data = pd.DataFrame(data, columns=list(map(str, range(len(data[0])))))
    return data


def image_svm(images_in, df, **kwargs):
    from sklearn.svm import SVC
    images = images_in[0]
    names = images_in[1]
    index = kwargs.pop('label')
    kernel = kwargs.pop('kernel')
    c_penalty = float(kwargs.pop('c_penalty'))
    allow_not_match = kwargs.pop('allow_not_match')
    try:
        label = df[index]
    except KeyError:
        label = df.iloc[:,0]
    data = images2df(images)
    if len(data) != len(label):
        if allow_not_match == 'False':
            raise Exception("Data and Label number not match")
        if len(data) > len(label):
            data = data[:len(label)]
        else:
            label = label[:len(data)]
    model = SVC(C=c_penalty, kernel=kernel)
    model = model.fit(data, label)
    return model

def image_svm_apply(skModel, images_in, **kwargs):
    import numpy as np
    import pandas as pd
    images = images_in[0]
    names = images_in[1]
    data = images2df(images)
    predict_label = kwargs.pop('predict_label')
    result = skModel.predict(data)
    names = np.array(names)
    data = np.stack([names, result], axis=1)
    df = pd.DataFrame(data, columns=['filename', predict_label])
    return df



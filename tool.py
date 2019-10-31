import os
import cv2
import json
import time
import random
import string
import filetype
import numpy as np
import pandas as pd
from functools import wraps

def msgwrap(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        ret = {
            'succeed':0,
            'message':'succeed',
        }
        try:
            result = func(*args, **kwargs)
            if type(result) is dict:
                ret.update(result)
        except Exception as e:
            print('error', e, flush=True)
            ret = {
                'succeed':1,
                'message':str(e),
            }
        return json.dumps(ret).encode('utf-8')
    return wrap

def gen_random_string(length=8, *, number=True, abc=True, upper_case=False, lower_case=False):
    charset = ''
    if number:
        charset += string.digits
    if abc:
        if upper_case==lower_case:
            charset += string.ascii_letters
        elif upper_case:
            charset += string.ascii_uppercase
        elif lower_case:
            charset += string.ascii_lowercase
    return ''.join(random.choice(charset) for _ in range(length))

def get_type(filepath=None, data=None):
    try:
        if filepath is not None:
            ans = filetype.guess_mime(filepath)
            print('filetype : ', filepath, ans)
            if ans is None:
                if filepath[-5:] == '.json':
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    if type(data) == list:
                        return 'Sequence'
                    return "Graph"
                elif filepath[-4:] == '.mat':
                    return 'Graph'
                elif filepath[-4:] == '.csv':
                    return "DataFrame"
                return "Text"
            if ans.find('image') != -1:
                return "Image"
            if ans.find('video') != -1:
                return 'Video'
            if ans.find('audio') != -1:
                return 'Audio'
        raise NotImplementedError
    except Exception as e:
        print("Guess Type Error :", e)
        print(filepath)

def safepath(path):
    # TODO : change replace
    path = path.replace('..', '')
    path = path.lstrip('/')
    path = path.replace('/', os.path.sep)
    return path

def sample_data(data, type_=None, num=10):
    if type_ == 'path':
        type_ = get_type(data)
        if type_ == 'DataFrame':
            data = [[pd.read_csv(data, nrows=10)], [os.path.basename(data)]]
        elif type_ == 'Image':
            data = cv2.imread(data)
        elif type_ == 'Sequence':
            with open(data, 'r') as f:
                data = json.load(f)
        elif type_ == 'Text':
            with open(data, 'r') as f:
                data = f.read()
        elif type_ == 'Graph':
            data = ''


    ret = {}
    if type_ == 'DataFrame':
        num = max(num, 0)
        index = list(data.columns)
        df = data[0:num]
        df = df.round(3)
        types = [str(df[index[j]].dtype) for j in range(len(index))]
        df = df.fillna('NaN')
        df = np.array(df).tolist()
        df = list(map(lambda x:list(map(lambda y:str(y) if len(str(y))< 16 else str(y)[:13]+'...',x)), df))
        if len(index) > 20:
            index = index[:19] + ['More...']
            df = list(map(lambda x:x[:19]+['...'], df))

        ret = {
            'type':'DataFrame',
            'shape':list(data.shape),
            'col_num':len(index),
            'col_index':index,
            'col_type':types,
            'row_num':num,
            'data': df
        }
    elif type_ == 'Image':
        savename = gen_random_string() + '.png'
        savedir = os.path.join('app', 'static', 'cache')
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        filename = data[1][0]
        data = data[0][0]
        shape = list(data.shape)
        shape[0], shape[1] = shape[1], shape[0]
        resize_shape = shape[:2]
        while resize_shape[0] > 640 or resize_shape[1] > 480:
            resize_shape[0] //= 2
            resize_shape[1] //= 2
        data = cv2.resize(data, tuple(resize_shape))
        cv2.imwrite(os.path.join(savedir, savename), data)
        ret = {
            'type':'Image',
            'data':{
                'url':'static/cache/'+savename,
                'shape':shape,
            }
        }
    elif type_ == 'Graph':
        ret = {
            'type':'Graph',
            'data':data,
        }
    elif type_ == 'Video':
        ret = {
            'type':'Video',
        }
    elif type_ == 'Sequence':
        data = data[:num]
        data = list(map(str, data))
        ret = {
            'type':'Sequence',
            'len':len(data),
            'data':data,
        }
    elif type_ == 'Text':
        ret = {
            'type':'Text',
            'data':data,
        }
    else:
        raise NotImplementedError
    print(ret)
    return ret

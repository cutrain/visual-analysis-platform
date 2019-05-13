import os
import json
from flask import render_template, request, send_file
import numpy as np
import pandas as pd

from config import DATA_DIR
from . import data
from tool import msgwrap, get_type, safepath, gen_random_string


@data.route('/upload', methods=['POST'])
@msgwrap
def upload():
    # TODO : return message
    global DATA_DIR
    path = request.form.get('dataset')
    path = safepath(path)
    file = request.files['file']
    path = os.path.join(DATA_DIR, path)
    file.save(path)
    return {
        "size":os.path.getsize(path),
        'type':get_type(path),
    }

@data.route('/createset', methods=['POST'])
@msgwrap
def createset():
    global DATA_DIR
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    path = req.pop('dataset')
    path = safepath(path)
    path = os.path.join(DATA_DIR, path)
    os.mkdir(path)

@data.route('/view', methods=['POST'])
@msgwrap
def view():
    global DATA_DIR
    def oswalk(obj, path):
        dirs = sorted(os.listdir(path))
        for i in dirs:
            new_path = os.path.join(path, i)
            if os.path.isdir(new_path):
                obj[i] = {}
                oswalk(obj[i], new_path)
        for i in dirs:
            new_path = os.path.join(path, i)
            if os.path.isfile(new_path):
                obj[i] = [os.path.getsize(new_path) // 1024, get_type(new_path)]
    structure = {}
    oswalk(structure, DATA_DIR)
    return {
        'structure':json.dumps(structure)
    }

@data.route('/get', methods=['POST'])
@msgwrap
def get():
    global DATA_DIR
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    path = safepath(req.pop('dataset'))
    name = safepath(req.pop('name'))
    path = os.path.join(DATA_DIR, path, name)
    if not os.path.exists(path):
        return {
            'succeed':0,
            'message':"File Not Exists",
        }
    if not os.path.isfile(path):
        return {
            'succeed':0,
            'message':path+ ' is not a file',
        }
    outtype = get_type(path)
    if outtype == 'DataFrame':
        idata = pd.read_csv(path, nrows=10)
        num = 10
        index = list(idata.columns)
        df = idata[0:num]
        df = df.round(3)
        types = [str(df[index[j]].dtype) for j in range(len(index))]
        df = df.fillna('NaN')
        df = np.array(df).tolist()
        ret = {
            'type':'DataFrame',
            'shape':list(idata.shape),
            'col_num':len(index),
            'col_index':index,
            'col_type':types,
            'row_num':num,
            'data': df
        }
    elif outtype == 'Image':
        import cv2
        savename = gen_random_string() + '.png'
        savedir = os.path.join('app', 'static', 'cache')
        if not os.path.exists(savedir):
            os.mkdir(savedir)
        idata = cv2.imread(path)
        shape = list(idata.shape)
        shape[0], shape[1] = shape[1], shape[0]
        resize_shape = shape[:2]
        while resize_shape[0] > 640 or resize_shape[1] > 480:
            resize_shape[0] //= 2
            resize_shape[1] //= 2
        idata = cv2.resize(idata, tuple(resize_shape))
        cv2.imwrite(os.path.join(savedir, savename), idata)
        ret = {
            'type':'Image',
            'data':{
                'url':'static/cache/'+savename,
                'shape':shape,
            }
        }
    elif outtype == 'Graph':
        ret = {
            'type':'Graph',
        }
    elif outtype == 'Video':
        ret = {
            'type':'Video',
        }
    else:
        raise NotImplementedError

    return ret

@data.route('/move', methods=['POST'])
@msgwrap
def move():
    global DATA_DIR
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    src = safepath(req.pop('src_path'))
    dest = safepath(req.pop('dest_path'))
    src = os.path.join(DATA_DIR, src)
    dest = os.path.join(DATA_DIR, dest)
    os.rename(src, dest)

@data.route('/delete', methods=['POST'])
@msgwrap
def delete():
    global DATA_DIR
    req = request.get_data().decode('utf-8')
    req = json.loads(req)
    path = safepath(req.pop('path'))
    path = os.path.join(DATA_DIR, path)
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.rmdir(os.path.join(root, dir))
        os.rmdir(path)
    else:
        os.remove(path)

@data.route('/download/<string:path>', methods=['GET'])
def download(path):
    print(path)
    global DATA_DIR
    path = safepath(path)
    path = os.path.join(os.getcwd(), DATA_DIR, path)
    return send_file(path, as_attachment=True)

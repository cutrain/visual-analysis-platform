import os
import json
from flask import render_template, request
import pandas as pd

from config import DATA_DIR
from . import data
from tool import msgwrap, get_type, safepath


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
                obj[i] = os.path.getsize(new_path) // 1024
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
    file_type = get_type(path)
    ret = {
        'type':file_type,
    }
    if file_type == 'DataFrame':
        data = pd.read_csv(path, nrows=10)
        ret['data'] = {
            'col_num':len(data.columns),
            'col_index':list(map(str,data.columns)),
            'col_type':list(map(str,list(data.dtypes))),
            'row_num':len(data),
            'data':data.values.tolist()
        }
    elif file_type == 'String':
        # TODO
        pass
    elif file_type == 'Image':
        # TODO
        pass
    else:
        # TODO
        pass

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
                os.removedirs(os.path.join(root, dir))
        os.removedirs(path)
    else:
        os.remove(path)


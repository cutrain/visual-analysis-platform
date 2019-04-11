import os
from flask import render_template, request
import pandas as pd

from config import data_dir
from . import data
from .. import db
from tool import msgwrap, get_type, safepath


@data.route('/upload', methods=['POST'])
@msgwrap
def upload():
    # TODO
    global data_dir
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    get_f = request['file']
    path = safepath(req.pop('dataset'))
    path = os.path.join(data_dir, path)
    with open(path, 'wb') as f:
        f.write(get_f)

    return {
        "size":213,
        'type':get_type(path)
    }

@data.route('/view', methods=['POST'])
@msgwrap
def view():
    global data_dir
    def oswalk(obj, path):
        dirs = sorted(os.listdir())
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
    oswalk(structure, data_dir)

@data.route('/get', methods=['POST'])
@msgwrap
def get():
    global data_dir
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    path = safepath(req.pop('path'))
    path = os.path.join(data_dir, path)
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
        with open(path, 'r') as f:
            data = pd.read_csv(file_type, nrows=10)
        ret['data'] = {
            'col_num':len(data.columns),
            'col_ndex':data.columns,
            'col_type':list(map(str,list(data.dtypes)))
            'row_num':len(data),
            'data':list(map(list, data.values))
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
    global data_dir
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    src = safepath(req.pop('src'))
    dest = safepath(req.pop('dest'))
    src = os.path.join(data_dir, src)
    dest = os.path.join(data_dir, dest)
    os.rename(src, dest)

@data.route('/delete', methods=['POST'])
@msgwrap
def delete():
    global data_dir
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    path = safepath(req.pop('path'))
    path = os.path.join(data_dir, path)
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                os.removedirs(os.path.join(root, dir))
        os.removedirs(path)
    else:
        os.remove(path)


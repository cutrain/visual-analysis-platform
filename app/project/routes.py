from . import project
from .. import db
from ..tool import msgwrap, gen_random_string
from flask import render_template, request

import os
import time
import json as js
import pickle

@project.route('/view', methods=['POST'])
@msgwrap
def view():
    ret = {}
    for root, dirs, files in os.walk('project'):
        for file in files:
            if file[-7:] == '.pickle':
                with open(os.path.join(root,file), 'rb') as f:
                    pj = pickle.load(f)
                ret[file[:-7]] = pj
    return ret

@project.route('/create', methods=['POST'])
@msgwrap
def create():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pname = req.pop('project_name')
    new_data = {
        'project_id':gen_random_string(8),
        'project_name':pname,
        'create_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }
    with open(os.path.join('project', new_data['project_id'] + '.pickle')) as f:
        f.write(pickle.dumps(new_data))
    ret = {
        'project_id':new_data['project_id']
    }
    return ret

@project.route('/change', methods=['POST'])
@msgwrap
def change():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    pname = req.pop('project_name')
    with open(os.path.join('project', pid+'.pickle'), 'rb') as f:
        data = pickle.load(f)
    data['project_name'] = pname
    with open(os.path.join('project', pid+'.pickle'), 'wb') as f:
        f.write(pickle.dumps(data))

@project.route('/delete', methods=['POST'])
@msgwrap
def delete():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    os.remove(os.path.join('project', pid+'.pickle'))


from config import PROJECT_DIR, DEBUG, logger
from . import project
from tool import msgwrap, gen_random_string
from flask import render_template, request

import os
import time
import json as js
import pickle

@project.route('/view', methods=['POST'])
@msgwrap
def view():
    global PROJECT_DIR
    ret = {}
    logger.info('project view : view')
    for root, dirs, files in os.walk(PROJECT_DIR):
        for file in files:
            if file[-7:] == '.pickle':
                with open(os.path.join(root,file), 'rb') as f:
                    pj = pickle.load(f)
                ret[file[:-7]] = pj
    logger.debug('project view return : {}',format(ret))
    return ret

@project.route('/create', methods=['POST'])
@msgwrap
def create():
    global PROJECT_DIR
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    logger.info('project create: {}'.format(req))
    pname = req.pop('project_name')
    new_data = {
        'project_id':gen_random_string(8),
        'project_name':pname,
        'create_time':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }
    if pname == 'temp':
        new_data['project_id'] = 'temp'
    with open(os.path.join(PROJECT_DIR, new_data['project_id'] + '.pickle'), 'wb') as f:
        f.write(pickle.dumps(new_data))
    ret = {
        'project_id':new_data['project_id']
    }
    logger.info('project create: succeed {}'.format(ret))
    return ret

@project.route('/change', methods=['POST'])
@msgwrap
def change():
    global PROJECT_DIR
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    logger.info('project change: {}'.format(req))
    pid = req.pop('project_id')
    pname = req.pop('project_name')
    with open(os.path.join(PROJECT_DIR, pid+'.pickle'), 'rb') as f:
        data = pickle.load(f)
    data['project_name'] = pname
    with open(os.path.join(PROJECT_DIR, pid+'.pickle'), 'wb') as f:
        f.write(pickle.dumps(data))
    logger.info('project change: succeed {}'.format(pid))

@project.route('/delete', methods=['POST'])
@msgwrap
def delete():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    logger.info('project delete: {}'.format(req))
    pid = req.pop('project_id')
    os.remove(os.path.join(PROJECT_DIR, pid+'.pickle'))
    logger.info('project delete: succeed {}'.format(pid))


from . import graph
from .. import db
from ..tool import msgwrap
from flask import render_template, request

from .analysis import analysis

import os
import redis
import pickle
import multiprocessing
import json as js
import pandas as pd
import numpy as np


debug = True

subprocess = multiprocessing.Process(name='empty')
r = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
r_data = redis.StrictRedis(host='localhost', db=0, port=6379)

@msgwrap
@graph.route('/get', methods=['POST'])
def get_graph():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    with open(os.path.join('project', pid+'.pickle'), 'rb') as f:
        p_data = pickle.load(f)
    G = p_data.pop('graph', {
        'all_nodes':'',
        'all_lines':'',
    })
    return G

@msgwrap
@graph.route('/save', methods=['POST'])
def save_graph():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    all_nodes = req.pop('all_nodes')
    all_lines = req.pop('all_lines')
    nodes_details = req.pop('nodes_details')
    with open(os.path.join('project', pid+'.pickle'), 'rb') as f:
        p_data = pickle.load(f)
    p_data.update({
        'all_nodes':all_nodes,
        'all_lines':all_lines,
    })
    with open(os.path.join('project', pid+'.pickle'), 'wb') as f:
        f.write(pickle.dumps(p_data))


@msgwrap
@graph.route('/run', methods=['POST'])
def run():
    # TODO
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    print(req)
    global child_process
    subprocess = multiprocessing.Process(name="analysis", target=analysis, args=(req,))
    subprocess.daemon = True
    subprocess.start()



@msgwrap
@graph.route('/progress', methods=['POST'])
def progress():
    # TODO
    progress = r.hgetall('status')
    print(progress)
    status = r.get('global')
    print(status)
    if status != '0':
        status = '1'

    tmp = {
        "status":status,
        "progress":progress
    }
    return tmp

@msgwrap
@graph.route('/stop', methods=['POST'])
def stop():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    # TODO


@msgwrap
@graph.route('/sample', methods=['POST'])
def sample():
    # TODO
    finish = False
    try:
        a = request.get_data().decode('utf-8')
        a = js.loads(a)
        df = pickle.loads(r_data.hget('data', a['node_name']+'out1'))
        num = max(a['number'], 0)
        num = min(num, len(df))
        index = df.columns.tolist()
        df = df[0:num]
        df = df.round(3)
        for i in range(len(index)):
            index[i] += '\n(' + str(df[index[i]].dtype) + ')'
        df = df.fillna('NaN')
        df = np.array(df).tolist()

        ret = {}
        ret = {
            'col':len(index),
            'index':index,
            'row':num,
            'data': df
        }
        finish = True

    except AttributeError as e:
        print('Error in route : sapmle Attribute')
        print(e)
        if type(df) is "list":
            df = df[0]
        ret = {
            'col':1,
            'index':['ErrorMessage'],
            'row':1,
            'data':[[str(df[0])]]
        }
    except Exception as e:
        print('Error in route : sapmle Exception')
        print(e)
        ret = {
            'col':1,
            'index':['ErrorMessage'],
            'row':1,
            'data':[[str(e)]]
        }
    if not finish and not debug:
        ret = {
            'col':0,
            'index':[],
            'row':0,
            'data':[],
            'message':ret['data']
        }

    return ret

@msgwrap
@graph.route('/init', methods=['POST'])
def init():
    print('init start')
    if subprocess.is_alive():
        subprocess.terminate()
    r.set('global', '1')
    r.delete('status')
    r.delete('data')


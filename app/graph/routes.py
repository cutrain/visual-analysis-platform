from . import graph
from .. import db
from ..tool import msgwrap
from flask import render_template, request

# from .analysis import analysis

import os
import redis
import pickle
import multiprocessing
import json as js
import pandas as pd
import numpy as np


debug = True

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)
r_data = redis.StrictRedis(host='localhost', db=0, port=6379)

processing_manager = {}

@graph.route('/get', methods=['POST'])
@msgwrap
def get_graph():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    with open(os.path.join('project', pid+'.pickle'), 'rb') as f:
        p_data = pickle.load(f)
    G = p_data.pop('graph', {
        'all_nodes':[],
        'all_lines':[],
    })
    return G

@graph.route('/save', methods=['POST'])
@msgwrap
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


@graph.route('/run', methods=['POST'])
@msgwrap
def run():
    # TODO: check format & create Graph as parameter
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    global processing_manager
    # check the project not running yet
    if pid in processing_manager:
        return {
            "succeed": 1,
            "message": "this project is running now",
        }
    process = multiprocessing.Process(name=pid, target=analysis, args=(req,))
    process.daemon = True
    process.start()
    processing_manager.update({
        pid: process
    })



@graph.route('/progress', methods=['POST'])
@msgwrap
def progress():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    global processing_manager
    status = 0
    if pid in processing_manager:
        status = 1
    progress = r.get('progress' + str(pid))
    print(pid + " nodes' status : ", status)

    ret = {
        "status":status,
        "progress":progress
    }
    return ret

@graph.route('/stop', methods=['POST'])
@msgwrap
def stop():
    req = request.get_data().decode('utf-8')
    req = js.loads(req)
    pid = req.pop('project_id')
    global processing_manager
    if pid not in processing_manager:
        return {
            "succeed": 1,
            "message": str(pid) + " not running",
        }
    processing_manager[pid].terminate()
    processing_manager.pop(pid)


@graph.route('/sample', methods=['POST'])
@msgwrap
def sample():
    # TODO
    a = request.get_data().decode('utf-8')
    a = js.loads(a)
    df = pickle.loads(r_data.hget('data', a['node_name']+'out1'))
    num = max(int(a['number']), 0)
    num = min(num, len(df))
    index = df.columns.tolist()
    df = df[0:num]
    df = df.round(3)
    types = [str(df[index[i]].dtype) for i in range(len(index))]
    df = df.fillna('NaN')
    df = np.array(df).tolist()

    ret = {
        'col_num':len(index),
        'col_index':index,
        'col_type':types,
        'row_num':num,
        'data': df
    }

    return ret

@graph.route('/init', methods=['POST'])
@msgwrap
def init():
    # TODO
    pass

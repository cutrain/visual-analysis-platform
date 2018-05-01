import redis
import pickle
import pandas as pd
import MySQLdb
import queue
from .algorithm import *
from .basic import *
from .data_process import *
from .others import *

r = redis.StrictRedis(host='localhost', port=6379, charset='utf-8', decode_responses=True)
r_data = redis.StrictRedis(host='localhost', port=6379)

from .api.inout import in0out1, in1out0, in1out1, in1out2, in2out1, in2out2

data = {}

# status : 0 finish 1 running 2 unvisited -1 failed

def run_nodes(args, in_degree):
    while True:
        runable = False
        dic = {}
        for node, t in args['all_nodes'].items():
            if r.hget('status', node) != "2":
                continue

            dic.update(
                {
                    'name':node,
                    'node_type':t,
                    'params':args['nodes_details'][node]
                }
            )

            if t in in0out1:
                r.hset('status', node, '1')
                runable = True
                break

            elif t in in1out0 or t in in1out1 or t in in1out2:
                in1 = node+'in1'
                if in1 not in in_degree:
                    r.hset('status', node, '-1')
                    continue
                if r.hget('status', in_degree[in1][:-4]) in ['1','2']:
                    continue
                if r.hget('status', in_degree[in1][:-4]) == "-1":
                    r.hset('status', node, '-1')
                r.hset('status', node, '1')
                dic.update({'in1':in_degree[in1]})
                runable = True
                break

            elif t in in2out1 or t in in2out2:
                in1 = node+'in1'
                in2 = node+'in2'
                if in1 not in in_degree or in2 not in in_degree:
                    r.hset('status', node, '-1')
                    continue
                if r.hget('status', in_degree[in1][:-4]) in ['1','2']:
                    continue
                if r.hget('status', in_degree[in1][:-4]) == "-1":
                    r.hset('status', node, '-1')
                if r.hget('status', in_degree[in2][:-4]) in ['1','2']:
                    continue
                if r.hget('status', in_degree[in2][:-4]) == "-1":
                    r.hset('status', node, '-1')
                r.hset('status', node, '1')
                dic.update({
                    'in1':in_degree[in1],
                    'in2':in_degree[in2]
                })
                runable = True
                break

            else:
                print("ERROR, unknown type found : " + t)

        if not runable:
            break
        yield dic

def single_mode(args, run_list):
    global data
    # delete unused data
    for node in run_list:
        data.pop(node, None)
    old_nodes = {}
    for node in data:
        old_nodes.update({node[:-4]:None})
    for node in args['all_nodes']:
        old_nodes.pop(node, None)
    for node in old_nodes:
        data.pop(node+'out1', None)
        data.pop(node+'out2', None)
    # check node state
    for node in old_nodes:
        if r.hexists('status', node):
            r.hdel('status', node)
    for node in args['all_nodes']:
        if not r.hexists('status', node):
            r.hset('status', node, '2')
    for node in run_list:
        r.hset('status', node, '2')
    # degree
    in_degree = {}
    for line, pair in args['all_lines'].items():
        in_degree[pair[1]] = pair[0]
    # get running node
    old_nodes = {}
    for node in args['all_nodes']:
        old_nodes.update({node:None})
    for node in run_list:
        old_nodes.pop(node, None)
    for node in old_nodes:
        args['all_nodes'].pop(node, None)
    q = run_nodes(args, in_degree)
    for node in q:
        yield node

def full_mode(args):
    global r, data
    # delete unused data
    data = {}
    # update node state
    r.delete('status')
    for node in args['all_nodes']:
        r.hset('status', node, '2')
    # check degree
    in_degree = {}
    for line, pair in args['all_lines'].items():
        in_degree[pair[1]] = pair[0]
    q = run_nodes(args, in_degree)
    for node in q:
        yield node


def analysis(args):
    """
    execute gragh according "all_nodes" "all_lines" "nodes_details"
    detail:
    1. delete old nodes which doesn't appear (use old nodes table)
    2. check runable state
    3. set new lines, degree setting & type check
    """
    global data
    r.set('global', '1')
    if r.exists('data'):
        tempdata = r_data.hgetall('data')
        for node in tempdata:
            data[node.decode('utf-8')] = pickle.loads(tempdata[node])
        del tempdata
    else:
        data = {}


    run_list = args.pop('run', None)
    if run_list is None:
        q = full_mode(args)
    else:
        q = single_mode(args, run_list)
    for node in q:
        run(**node)
    for node in data:
        r_data.hset('data', node, pickle.dumps(data[node]))
    r.set('global', '0')


def run(name, node_type, params, in1=None, in2=None):
    global data
    print('running', name)
    if node_type in in0out1:
        b, result = run_func(node_type, params=params)
        data[name + 'out1'] = result
    elif node_type in in1out0:
        b, tmp = run_func(node_type, in1=data[in1], params=params)
    elif node_type in in1out1:
        b, result = run_func(node_type, in1=data[in1], params=params)
        data[name + 'out1'] = result
    elif node_type in in1out2:
        b, results = run_func(node_type, in1=data[in1], params=params)
        data[name + 'out1'] = results[0]
        data[name + 'out2'] = results[1]
    elif node_type in in2out1:
        b, result = run_func(node_type, in1=data[in1], in2=data[in2], params=params)
        data[name + 'out1'] = result
    elif node_type in in2out2:
        b, results = run_func(node_type, in1=data[in1], in2=data[in2], params=params)
        data[name + 'out1'] = results[0]
        data[name + 'out2'] = results[1]
    else:
        print("ERROR, unknown type found : " + node_type)

    if b:
        r.hset('status', name, '0')
    else:
        r.hset('status', name, '-1')

def run_func(node_type, params=None, in1=None, in2=None):
    s = node_type.replace('-', '_')
    return eval(s + '(in1=in1, in2=in2, **params)')



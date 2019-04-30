import os
import time
import json
import pickle
import redis

import threading
import multiprocessing
from queue import Queue
# from multiprocessing import Queue
from collections import defaultdict

from config import CACHE_DIR, REDIS_PORT, REDIS_DB, REDIS_HOST
from .algorithm import *
from common import component_detail
from functools import wraps


def func_pack(func, *args, **kwargs):
    @wraps(func)
    def wrap(*args, **kwargs):
        result = func(*args, **kwargs)
        if type(result) != tuple:
            result = (result,)
        return result
    return wrap

class Port:
    def __init__(self, node, data_type):
        self.node = node
        self._data_type = data_type
        self._data = None

    def __call__(self, data=None):
        if data is not None:
            # TODO : check data type
            self._data = data
        return self._data

    def __repr__(self):
        ret = 'Port of Node : ' + self.node._name + ' Type : ' + self._data_type + ' Data : '
        ret += repr(self._data)
        return ret

    def reset(self):
        self._data = None

    @property
    def type(self):
        return self._data_type

class Node:
    # status: 0:finish 1:wait 2:running -1:fail
    def __init__(self, node_name, node_type, param):
        global component_detail
        self.status = 1
        self._name = node_name
        self._detail = component_detail[node_type]
        self._in_port_name = [None for i in self._detail['in_port'] ]
        self._in_port = [None for i in self._detail['in_port'] ]
        self._in = [Port(self, i) for i in self._detail['in_port'] ] # will not use it, just for type check
        self._out = [Port(self, i) for i in self._detail['out_port'] ]
        self._param = param
        # TODO : check param avaliable
        print('node :', self._name, 'function :', node_type, eval(node_type), flush=True)
        self._func = func_pack(eval(node_type))
        self._thread = None

    @property
    def data(self):
        return self._out

    def save(self, dirpath):
        data = {
            'name':self._name,
            'detail':self._detail,
            'status':self.status,
            'in_port_name':self._in_port_name,
            'out':list(map(lambda x:x(), self._out)),
            'param':self._param,
        }
        if not os.path.exists(dirpath):
            os.mkdir(dirpath)
        with open(os.path.join(dirpath, self._name + '.pickle'), 'wb') as f:
            f.write(pickle.dumps(data))

    def load(self, dirpath):
        try:
            with open(os.path.join(dirpath, self._name + '.pickle'), 'rb') as f:
                data = pickle.load(f)
            if data['name'] != self._name:
                print("ERROR: Node load, unexpect error happend")
                return
            if data['detail'] != self._detail:
                print('load error, detail changed :', self._name, self._detail, data['detail'])
                return
            if data['param'] != self._param:
                print('param changed :', self._name, self._param, data['param'])
                return
            if not all(map(lambda x:x[0]==x[1], zip(data['in_port_name'], self._in_port_name))):
                print('in port not match :', self._name, self._in_port_name, data['in_port_name'])
                return
            self.status = data['status']
            for i in range(len(self._out)):
                self._out[i](data['out'][i])
            return True
        except Exception as e:
            print('node', self._name, 'load fail', e)
            return False

    def reset(self):
        self.status = 1
        for i in self._out:
            i.reset()

    def stop(self):
        self._thread.terminate()

    def __run(self):
        try:
            print('node', self._name, 'start run', flush=True)
            self.status = 2
            result = self._func(*tuple(map(lambda x:x(), self._in_port)), **self._param)
            print('node', self._name, 'finish running', flush=True)
            for i in range(len(self._out)):
                self._out[i](result[i])
            self.status = 0
            print('node', self._name, 'get ans', flush=True)
        except Exception as e:
            print('node', self._name, 'running break', flush=True)
            print('Node Run Error :', self)
            print(e)
            self.status = -1

    def __call__(self):
        try:
            # check inport exists
            if not all(self._in_port):
                self.status = -1
                return

            # check inport not fail
            if not all(map(lambda x:x.node.status != -1, self._in_port)):
                self.status = -1
                return

            # check inport ready
            if not all(map(lambda x:x.node.status == 0, self._in_port)):
                return

            # start running
            self._thread = threading.Thread(target=self.__run)
            self._thread.daemon = True
            self._thread.start()
        except Exception as e:
            print('Node Call Error :', self)
            print(e)
            self.status = -1

    def __repr__(self):
        ret = ''
        ret += 'Node name : ' + str(self._name)
        ret += ' Node type : ' + str(self._detail['name'])
        ret += ' Status : ' + str(self.status)
        ret += ' in port data : ' + str(list(map(repr, self._in_port)))
        ret += ' out port data : ' + str(list(map(repr, self._out)))
        ret += ' Params : ' + str(self._param)
        return ret

class Graph:
    def __init__(self, pid):
        self.pid = pid
        self.nodes = {}

    def add_node(self, node_name, node_type, param):
        try:
            self.nodes[node_name] = Node(node_name, node_type, param)
            return True
        except Exception as e:
            print('add node error :', e)
        return False

    def add_edge(self, node_from, port_from, node_to, port_to):
        try:
            if self.nodes[node_to]._in[port_to].type == self.nodes[node_from]._out[port_from].type:
                self.nodes[node_to]._in_port_name[port_to] = node_from + '-' + str(port_from)
                self.nodes[node_to]._in_port[port_to] = self.nodes[node_from]._out[port_from]
                return True
        except Exception as e:
            print('add edge error :', e)
        return False

    def load_cache(self):
        try:
            global CACHE_DIR
            for key in self.nodes:
                self.nodes[key].load(os.path.join(CACHE_DIR, self.pid))
            changed = True
            while changed:
                changed = False
                for key in self.nodes:
                    node = self.nodes[key]
                    if node.status == -1:
                        node.status = 1
                    if node.status == 0:
                        for port in node._in_port:
                            if port.node.status != 0:
                                node.reset()
                                changed = True

            # Delete nouse cache
            for key in self.nodes:
                node = self.nodes[key]
                path = os.path.join(CACHE_DIR, self.pid, node._name+'.pickle')
                if node.status != 0:
                    if os.path.exists(path):
                        os.remove(path)
                        print('delete unused cache', path)

            return True
        except Exception as e:
            print('load cache error :', e)
        return False

    def __call__(self, run_node=None):
        global REDIS_HOST, REDIS_PORT, REDIS_DB
        self.r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, charset='utf-8', decode_responses=True)
        for key, val in self.nodes.items():
            self.r.hset(self.pid, key, val.status)

        # get which nodes to run
        last = {}
        if not run_node:
            for key, val in self.nodes.items():
                last.update({key:val})
        else:
            for key in run_node:
                if key in self.nodes:
                    print(key)
                    print(self.nodes[key], flush=True)
                    last.update({key : self.nodes[key]})
                    self.nodes[key].status = 1

        # ensure pre node
        changed = True
        while changed:
            changed = False
            new_dict = {}
            for key, val in last.items():
                for pre in val._in_port:
                    if pre is not None:
                        name = pre.node._name
                        if name not in last:
                            new_dict.update({name : self.nodes[name]})
                            changed = True
            last.update(new_dict)


        class wait_scheduler:
            def __init__(self, init=0.1, times=1.5, upper_bound=1):
                self.__init = init
                self.__wait = init
                self.__times = times
                self.__upper_bound = upper_bound
                self.__cnt = 0

            def __call__(self, reset=False):
                if reset != False:
                    self.__cnt = 0
                    self.__wait = self.__init
                else:
                    self.__wait = self.__wait * self.__times
                    self.__wait = min(self.__wait, self.__upper_bound)
                time.sleep(self.__wait)

        ws = wait_scheduler()
        while len(last.keys()) > 0:
            print('graph monitor loop')
            delkey = []
            wait = True
            for key, val in last.items():
                if val.status == 1:
                    val()
                elif val.status == 0:
                    print('saving')
                    val.save(os.path.join(CACHE_DIR, self.pid))
                    delkey.append(key)
                elif val.status == -1:
                    delkey.append(key)
                elif val.status == 2:
                    pass
                else:
                    print('ERROR!!! UNKNOWN RUNNING STATUS', val.status)
            for ikey in delkey:
                print('stop node', ikey)
                last.pop(ikey)
                wait = False
            for key,val in self.nodes.items():
                self.r.hset(self.pid, key, val.status)
            # TODO : find better stuck method
            ws(not wait)
        print('graph end')


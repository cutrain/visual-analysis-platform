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
    def wrap(queue, *args, **kwargs):
        result = func(*args, **kwargs)
        if type(result) is tuple:
            for i in result:
                queue.put(result)
                print('put')
        else:
            queue.put(result)
        print('put all')
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
        print(self._func)
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
        with open(os.path.join(dirpath, self._name + '.pickle'), 'wb') as f:
            f.write(pickle.dumps(data))

    def load(self, dirpath):
        try:
            with open(os.path.join(dirpath, self._name + '.pickle'), 'rb') as f:
                data = pickle.load(f)
            if data['name'] != self._name:
                print("ERROR: Node load, unexpect error happend")
                return
            if cmp(data['detail'], self._detail) != 0:
                print('load error, detail changed :', self._name, self._detail, data['detail'])
                return
            if cmp(data['param'], self._param) != 0:
                print('param changed :', self._name, self._param, data['param'])
                return
            if not all(map(lambda x:x[0]==x[1], (data['in_port_name'], self._in_port_name))):
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
            self._queue = Queue()
            # self._processing = multiprocessing.Process(target=self._func, args=(self._queue,) + tuple(map(lambda x:x(), self._in_port)), kwargs=self._param)
            self._processing = threading.Thread(target=self._func, args=(self._queue,) + tuple(map(lambda x:x(), self._in_port)), kwargs=self._param)
            self._processing.daemon = True
            print('node', self._name, 'start run', flush=True)
            self._processing.start()
            self.status = 2
            self._processing.join()
            print('node', self._name, 'finish running', flush=True)
            del self._processing
            for i in range(len(self._out)):
                self._out[i](self._queue.get())
            # self._queue.close() # multiprocessing use this
            self.status = 0
            del self._queue
            print('node', self._name, 'get ans', flush=True)
        except Exception as e:
            print('node', self._name, 'run break', flush=True)
            # self._queue.close() # multiprocessing use this
            print('Node Run Error :')
            self.__repr__(indent=4)
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
            print('Node Call Error :')
            self.__repr__(indent=4)
            print(e)
            self.status = -1

    def __repr__(self, *, indent=0):
        print(' '*indent + 'node name :', self._name)
        print(' '*indent + 'node type :', self._detail['name'])
        print(' '*indent + 'status :', self.status)
        print(' '*indent + 'in port data :', list(map(lambda x:x(), self._in_port)))
        print(' '*indent + 'out port data :', list(map(lambda x:x(), self._out)))
        print(' '*indent + 'params :', self._param)

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
                self.nodes[node_to]._in_port_name[port_to] = node_from + '-' + port_from
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
            return True
        except Exception as e:
            print('load cache error :', e)
        return False

    def __call__(self):
        global REDIS_HOST, REDIS_PORT, REDIS_DB
        self.r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, charset='utf-8', decode_responses=True)
        for key, val in self.nodes.items():
            self.r.hset(self.pid, key, val.status)
        last = {}
        for key, val in self.nodes.items():
            last.update({key:val})

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
                else:
                    delkey.append(key)
            for i in delkey:
                print('stop node', i)
                last.pop(i)
                wait = False
            for key,val in self.nodes.items():
                self.r.hset(self.pid, key, val.status)
            # TODO : find better stuck method
            ws(not wait)
        print('graph end')


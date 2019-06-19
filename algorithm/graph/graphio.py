import networkx as nx
from networkx.readwrite import json_graph
import json
import scipy.io as scio


def from_json_dicts(file_path):
    '''
    :param file_path:文件路径
    :return: graph:无向图
    '''
    graph = None
    try:
        with open(file_path, 'r') as file:
            graph_str = file.read()
    except FileNotFoundError:
        print("文件不存在，请检查路径")
    else:
        try:
            graph_json = json.loads(graph_str)
        except json.decoder.JSONDecodeError:
            print("请输入标准格式的json文件")
        else:
            try:
                graph = nx.from_dict_of_dicts(graph_json)
            except AttributeError:
                print("节点没有属性，空节点必须加上':{}'")
    finally:
        return graph


def from_json_lists(file_path):
    '''
    :param file_path:文件路径
    :return: graph:无向图
    '''
    graph = None
    try:
        with open(file_path, 'r') as file:
            graph_str = file.read()
    except FileNotFoundError:
        print("文件不存在，请检查路径")
    else:
        try:
            graph_json = json.loads(graph_str)
        except json.decoder.JSONDecodeError:
            print("请输入标准格式的json文件")
        else:
            try:
                graph = nx.from_dict_of_lists(graph_json)
            except TypeError:
                print("属性类型不支持")
    finally:
        return graph


def from_mat_matrix(file_path, name=None):
    '''
    :param file_path:
    :param name:
    :return: graph:无向图
    '''
    graph = None
    if name is None:
        name = 'adj'
    try:
        mat = scio.loadmat(file_path)
    except FileNotFoundError:
        print("文件不存在，请检查路径")
    else:
        if not (name in mat.keys()):
            print("键不存在")
        adj = mat[name]
        graph = nx.from_numpy_matrix(adj)
    finally:
        return graph


def to_json_dicts(file_path, graph):
    '''
    nx.Graph写成json
    :param file_path: json文件名
    :param graph: nx.Graph
    :return:
    '''
    graph_json = nx.to_dict_of_dicts(graph)
    str = json.dumps(graph_json)
    with open(file_path, 'w') as file:
        file.write(str)


def to_json_lists(file_path, graph):
    '''
    nx.Graph写成json
    :param file_path: json文件名
    :param graph: nx.Graph
    :return:
    '''
    graph_json = nx.to_dict_of_lists(graph)
    str = json.dumps(graph_json)
    with open(file_path, 'w') as file:
        file.write(str)


def to_mat_matrix(file_path, graph, name=None):
    '''
    把nx.Graph写成mat文件，键值为name
    :param file_path:
    :param graph:
    :param name:
    :return:
    example:
        >>> import graphio.graphio as gio
        >>> import numpy as np
        >>> import networkx as nx
        >>> graph = nx.from_numpy_matrix(np.array([[1,0],[0,1]]))
        >>> gio.to_mat_matrix('example_mat.mat',graph)
    '''
    if name is None:
        name = 'adj'
    graph_dict = {name: nx.to_numpy_matrix(graph)}
    scio.savemat(file_path, graph_dict)


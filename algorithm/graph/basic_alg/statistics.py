import collections
import networkx as nx
import numpy as np
import pandas as pd
import scipy.sparse as sp

def gms2graph(graph):
    '''
    np.ndarray,np.matrix,sparse_matrix转nx.graph
    :param graph:
    :return:
    example:
        >>> from graph_utils import *
        >>> adj = np.array([[1,0],[0,1]])
        >>> print(type(adj))
        <class 'numpy.ndarray'>
        >>> graph = gms2graph(adj)
        >>> print(type(graph))
        <class 'networkx.classes.graph.Graph'>
    '''
    if isinstance(graph, (np.ndarray, np.matrix)):
        graph = nx.from_numpy_matrix(graph)
    if sp.isspmatrix(graph):
        graph = nx.from_scipy_sparse_matrix(graph)
    return graph

def _count_triangles(graph):
    '''
    数三角形,返回一个字典{节点名：三角数目}
    :param graph:
    :return:
    '''
    graph = gms2graph(graph)
    return nx.triangles(graph)


def count_triangles(graph):
    return pd.DataFrame.from_dict(_count_triangles(graph), orient='index', columns=['number'])


def _count_k_cycles(graph, k):
    '''
    数k圈，会有重复节点{节点名：k-cycles数目}
    :param graph:
    :param k:
    :return:
    '''
    num = None
    if (k > 1):
        num = {}
        graph = gms2graph(graph)
        adj_ori = nx.to_scipy_sparse_matrix(graph)
        adj = nx.to_scipy_sparse_matrix(graph)
        for i in range(k - 1):
            adj = adj.dot(adj_ori)
        i = 0
        for node in graph.nodes:
            num[node] = adj[i, i] // 2
            i += 1
    else:
        print("k必须大于1")
    return num


def count_k_cycles(graph, k):
    return pd.DataFrame.from_dict(_count_k_cycles(graph, k), orient='index', columns=['number'])


if __name__ == '__main__':
    graph_dict = {"22": [1, 2], 2: [1, 3, 4], 3: [4, 5], 4: [5]}
    graph = nx.from_dict_of_lists(graph_dict)
    num_triangles = count_triangles(graph)
    num_quadrangles = count_k_cycles(graph, 3)
    pass

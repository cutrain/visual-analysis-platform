import networkx as nx
import numpy as np
import scipy.sparse as sp
import pandas as pd


def k_core_subgraph(graph, k):
    '''
    返回k-core子图
    :param graph:
    :param k:
    :return:

    example:
        输入nx.Graph:
            >>> import algorithm.community as com
            >>> import networkx as nx
            >>> graph_dict = {"sas": [1, 2, 3, 4], 2: [3, 4, 5], 5: [6], 6: [7], 3: [4]}
            >>> graph1 = nx.from_dict_of_lists(graph_dict)
            >>> subgraph1 = com.k_core_subgraph(graph1,3)
            >>> print(subgraph1.nodes)
            ['sas', 2, 3, 4]
        输入numpy.ndarray或者numpy.matrix:
            >>> adj = nx.to_numpy_matrix(graph1)
            >>> print(adj)
            [[0. 1. 0. 0. 1. 1. 1. 0.]
             [1. 0. 1. 0. 1. 0. 1. 0.]
             [0. 1. 0. 1. 0. 0. 0. 0.]
             [0. 0. 1. 0. 0. 0. 0. 1.]
             [1. 1. 0. 0. 0. 0. 1. 0.]
             [1. 0. 0. 0. 0. 0. 0. 0.]
             [1. 1. 0. 0. 1. 0. 0. 0.]
             [0. 0. 0. 1. 0. 0. 0. 0.]]
            >>> subgraph1 = com.k_core_subgraph(adj,3)
            >>> print(subgraph1.nodes)
            [0, 1, 4, 6]
        输入scipy.sparse下的csr,csc等稀疏矩阵:
            >>> adj_sparse = nx.to_scipy_sparse_matrix(graph1)
            >>> print(adj_sparse)
              (0, 1)	1
              (0, 4)	1
              (0, 5)	1
              (0, 6)	1
              (1, 0)	1
              (1, 2)	1
              (1, 4)	1
              (1, 6)	1
              (2, 1)	1
              (2, 3)	1
              (3, 2)	1
              (3, 7)	1
              (4, 0)	1
              (4, 1)	1
              (4, 6)	1
              (5, 0)	1
              (6, 0)	1
              (6, 1)	1
              (6, 4)	1
              (7, 3)	1
            >>> subgraph1 = com.k_core_subgraph(adj_sparse,3)
            >>> print(subgraph1.nodes)
            [0, 1, 4, 6]
    '''
    subgraph = None
    if isinstance(graph, nx.Graph):
        try:
            subgraph = nx.algorithms.k_core(graph, k)
        except nx.NetworkXError:
            print("图中不能存在多重边或者自环")
        finally:
            pass
    elif isinstance(graph, (np.ndarray, np.matrix)):
        graph = nx.from_numpy_matrix(graph)
        subgraph = nx.algorithms.k_core(graph, k)
    elif sp.isspmatrix(graph):
        graph = nx.from_scipy_sparse_matrix(graph)
        subgraph = nx.algorithms.k_core(graph, k)
    return subgraph


def k_core_name_list(graph, k):
    '''
    返回k-core子图的节点名称，如果输入是nx.Graph则返回字符，如果是矩阵则返回对应的序号
    :param graph:
    :param k:
    :return:

    example:
        输入是nx.Graph:
            >>> import algorithm.community as com
            >>> import networkx as nx
            >>> graph_dict = {"sas": [1, 2, 3, 4], 2: [3, 4, 5], 5: [6], 6: [7], 3: [4]}
            >>> graph1 = nx.from_dict_of_lists(graph_dict)
            >>> name_list = com.k_core_name_list(graph1,3)
            >>> print(name_list)
            ['sas', 2, 3, 4]
        输入是矩阵:
            >>> adj = nx.to_numpy_matrix(graph1)
            >>> print(adj)
            [[0. 1. 0. 0. 1. 1. 1. 0.]
             [1. 0. 1. 0. 1. 0. 1. 0.]
             [0. 1. 0. 1. 0. 0. 0. 0.]
             [0. 0. 1. 0. 0. 0. 0. 1.]
             [1. 1. 0. 0. 0. 0. 1. 0.]
             [1. 0. 0. 0. 0. 0. 0. 0.]
             [1. 1. 0. 0. 1. 0. 0. 0.]
             [0. 0. 0. 1. 0. 0. 0. 0.]]
            >>> name_list = com.k_core_name_list(adj,3)
            >>> print(name_list)
            [0, 1, 4, 6]
    '''
    name_list = None
    subgraph = k_core_subgraph(graph, k)
    if not subgraph is None:
        name_list = [x for x in subgraph.node]
    return name_list


def _pagerank(graph, alpha=0.85):
    '''
    返回字典，{节点:概率}
    :param graph:
    :param alpha:
    :return:
    example:
        >>> import algorithm.community as com
        >>> graph = nx.from_numpy_matrix(np.array([[1,0],[0,1]]))
        >>> com.pagerank(graph)
        {0: 0.5, 1: 0.5}
    '''
    return nx.pagerank(graph, alpha)


def pagerank(graph, alpha=0.85):
    return pd.DataFrame.from_dict(_pagerank(graph, alpha), orient='index', columns=['rank'])


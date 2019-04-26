import networkx as nx
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


def from_mat_matrix(file_path, name):
    '''
    :param file_path:
    :param name:
    :return: graph:无向图
    '''
    graph = None
    try:
        mat = scio.loadmat(file_path)
    except FileNotFoundError:
        print("文件不存在，请检查路径")
    else:
        if not(name in mat.keys()):
            print("键不存在")
        adj = mat[name]
        graph = nx.from_numpy_matrix(adj)
    finally:
        return graph

def graph2json(graph):
    return nx.to_dict_of_dicts(graph)


if __name__ == "__main__":
    graph1 = from_json_dicts('example_dicts.json')
    # graph2 = from_json_lists('example_lists.json')
    graph3 = from_mat_matrix('example_adj.mat', 'a')
    pass

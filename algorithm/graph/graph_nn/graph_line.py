__all__ = [
    'graph_line',
]

import networkx

def graph_line(graph, **kwargs):
    from ._line import LINE, Graph
    import pandas as pd
    new_graph = graph.copy()
    print('3')
    for e in new_graph.edges():
        print(e)
        try:
            print(type(new_graph[e[0]][e[1]]))
            new_graph[e[0]][e[1]]['weight'] = 1
        except Exception as err:
            print(err)
    print('4')
    g = Graph()
    g.read_g(new_graph)
    model = LINE(g, epoch=1, rep_size=128, order=3)
    df = pd.DataFrame(columns=['node', 'vector'])
    for node, vec in model.vectors.items():
        df = df.append({'node': node, 'vector': vec}, ignore_index=True)
    return df

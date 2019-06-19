
__all__ = [
    'graph_kcore',
    'graph_count_triangle',
    'graph_count_kcycle',
    'graph_pagerank',
]

def graph_kcore(graph, **kwargs):
    from .basic_alg.community import k_core_subgraph
    k = int(kwargs.pop('k'))
    result = k_core_subgraph(graph, k=k)
    return result

def graph_count_triangle(graph, **kwargs):
    from .basic_alg.statistics import count_triangles
    result = count_triangles(graph)
    return result

def graph_count_kcycle(graph, **kwargs):
    from .basic_alg.statistics import count_k_cycles
    k = int(kwargs.pop('k'))
    result = count_k_cycles(graph, 3)
    return result

def graph_pagerank(graph, **kwargs):
    from .basic_alg.community import pagerank
    alpha = float(kwargs.pop('alpha'))
    result = pagerank(graph, alpha)
    return result


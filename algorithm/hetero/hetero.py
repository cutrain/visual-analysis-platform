__all__ = [
    'hetero_metapath2vec',
    'hetero_line',
]

def hetero_metapath2vec(data, **kwargs):
    import pandas as pd
    from .metapath2vec import Meta2Vec
    m = Meta2Vec()
    m.df = data
    m.init_model()
    m.train_model(10, 10, 5, None, num_iter=1, rewalk=True)
    nd = m.get_emb_df()
    df = pd.DataFrame(nd)
    return df

def hetero_line(data, ** kwargs):
    import pandas as pd
    from .line import Graph, LINE
    g = Graph()
    g.read_graph(data)
    model = LINE(g, epoch=100, rep_size=128, order=3)
    df = pd.DataFrame(columns=['node', 'vector'])
    for node, vec in model.vectors.items():
        df = df.append({'node': node, 'vector':vec}, ignore_index=True)
    return df



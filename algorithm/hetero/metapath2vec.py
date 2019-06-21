'''
如果报错AttributeError: 'HeteGraph' object has no attribute 'edge'，
是因为networkx包太新了，没有其他解决方案，只能安装版本为1.11networkx的包;
参数说明：
传入建图数据为CSV格式的基因-疾病-miRNA交互数据（异质），
每行记录格式为['node1','node1_type','node2','node2_type','weight'];
rep_size是生成向量的维度，默认128；
其他参数默认即可；
'''




import pandas as pd
from networkx.classes.graph import Graph
import networkx as nx
from networkx.exception import NetworkXError
import random
from itertools import cycle,dropwhile
from functools import reduce
import operator
from gensim.models import Word2Vec



#generate data for the platform
# class Gen_data(object):
#     def __init__(self):
#         self.df = pd.DataFrame()
#     def load_edges(self, filepath, lost_type=False,sam_rate=1.0):
#         if not lost_type:
#             df = pd.read_csv(filepath, header=None,
#             names=['node1','node1_type',
#             'node2','node2_type','weight'], dtype=str)
#         else:
#             df = pd.read_csv(filepath, header=None,
#                              names=['node1',
#                                     'node2', 'weight'], dtype=str)
#             df['node1_type']='miRNA'
#             df['node2_type']='miRNA'
#         df = df.sample(frac=sam_rate)
#         self.df=self.df.append(df)
#
# ge=Gen_data()
# ge.load_edges('./data/DD_MinMiner_0.5.csv')
# ge.load_edges('./data/MM_misim_0.5.csv', lost_type=True)
# ge.load_edges('./data/MD_Verified242_miRNet.csv')
# ge.load_edges('./data/GG_HPRD.csv',sam_rate=0.2)
# ge.load_edges('./data/MG_miRTarBase_strong.csv')
# ge.load_edges('./data/GD_DisGeNET_0.3.csv')
# ge.df.to_csv('./dmg_small.csv',index=False,header=None)



def gen_filter_func(key, op, val):
    def get_op(inp, relate, cut):
        ops = {'>': operator.gt,
               '<': operator.lt,
               '>=': operator.ge,
               '<=': operator.le,
               '==': operator.eq,
               '!=': operator.ne}
        return ops[relate](inp, cut)

    return lambda x: get_op(x[key], op, val)


def combine_func(funcs):
    return reduce(lambda fx, fy: lambda x: fx(x) and fy(x), funcs)


# def list_intersect(lists):
#     return list(set(lists[0]).intersection(*lists))

class HeteGraph(Graph):
    def nodes_iter(self, data=False, default=None, filterFunc=None):
        if data is True:
            for n, ddict in self.node.items():
                if filterFunc and not filterFunc(self.node[n]):
                    continue
                else:
                    yield (n, ddict)
        elif data is not False:
            for n, ddict in self.node.items():
                if filterFunc and not filterFunc(self.node[n]):
                    continue
                else:
                    d = ddict[data] if data in ddict else default
                    yield (n, d)

        else:
            for n in self.node:
                if filterFunc and not filterFunc(self.node[n]):
                    continue
                else:
                    yield n

    def nodes(self, data=False, default=None, filterFunc=None):
        return list(self.nodes_iter(data=data, default=default, filterFunc=filterFunc))

    def neighbors(self, n, data=False, default=None, filterFunc=None):
        try:
            neighbors = list(self.adj[n])
            if filterFunc:
                neighbors = list(filter(lambda x: filterFunc(self.node[x]), neighbors))

            neighbors_dict = [(x, self.node[x]) for x in neighbors]
            if data is True:
                rst = neighbors_dict
            elif data is not False:
                rst = [(x, ddict[data]) if data in ddict else (x, default) for (x, ddict) in neighbors_dict]
            else:
                rst = neighbors

            return rst
        except KeyError:
            raise NetworkXError("The node %s is not in the graph." % (n,))

    def load_edgelist(self, file_):
        with open(file_) as f:
            cnt = 0
            for l in f:
                node1, node1_type, \
                node2, node2_type, weight \
                    = l.strip().split(',')
                self.add_node(node1, type=node1_type)
                self.add_node(node2, type=node2_type)
                self.add_edge(node1, node2, weight=float(weight))
                cnt += 1
                # logger.info("add %i edges.", cnt)

    def load_dataframe(self, df):
        def load_single_entry(x):
            self.add_node(x['node1'], type=x['node1_type'])
            self.add_node(x['node2'], type=x['node2_type'])
            self.add_edge(x['node1'], x['node2'], weight=float(x['weight']))

        df.apply(load_single_entry, axis=1)
        # logger.info("add %i edges.", len(df))

    def random_walk(self, metapath, path_length, start, rand=random.Random()):
        G = self
        # print(G.edges())
        if metapath:
            path_type_iter = dropwhile(lambda x: x != G.node[start]['type'], cycle(metapath))
            next(path_type_iter)

        path = [start]

        while len(path) < path_length:
            cur = path[-1]
            filterFunc = None
            if metapath:
                cur_type = G.node[cur]['type']
                next_type = next(path_type_iter)
                filterFunc = gen_filter_func('type', '==', next_type)

            neighbors = G.neighbors(cur, filterFunc=filterFunc)

            if len(neighbors) > 0:
                weighted = {k: v['weight'] if k in neighbors else 0 for (k, v) in G.edge[cur].items()}
                next_node = nx.utils.weighted_choice(weighted)
                path.append(next_node)
            else:
                return None
        return path

    def build_corpus(self, num_walks, path_length, metapath=None, rand=random.Random()):
        G = self
        nodes = G.nodes()
        walks = []
        for cnt in range(num_walks):
            # logger.info("Walk Iter:{cnt}/{total}".format(cnt=cnt+1,total=num_walks))
            rand.shuffle(nodes)
            for node in nodes:
                if metapath and G.node[node]['type'] not in metapath:
                    continue
                walk = G.random_walk(metapath, path_length, node)
                if walk:
                    walks.append(walk)
        return walks


class Meta2Vec(object):
    def __init__(self):
        self.df = pd.DataFrame()
        # self.train = pd.DataFrame()
        # self.test = pd.DataFrame()
        self.path_dict = {}
    def load_edges(self, filepath):
        df=pd.read_csv(filepath,header=None,names=['node1','node1_type','node2','node2_type','weight'], dtype=str)
        self.df=df

    def build_graph(self):
        G = HeteGraph()
        G.load_dataframe(self.df)
        #logger.info("build graph with %i nodes and %i edges.", len(G.nodes()), len(G.edges()))
        self.graph = G


    def init_model(self):
        if not hasattr(self, 'graph'):
            #logger.info("build graph before train model.")
            self.build_graph()

        # if hasattr(self, 'model'):
        #     logger.info("reset model.")
        model = Word2Vec(size=128, min_count=1, sample=0, sg=1, hs=0, negative=5)
        self.model = model

    def train_model(self, num_walks, path_length, window, metapath, num_iter=1, rewalk=True, graph=None):
        if not hasattr(self, 'model'):
            #logger.warning("Please init model before train model.")
            return

        model = self.model
        if not graph:
            graph = self.graph

        if metapath in self.path_dict and not rewalk:
            walks = self.path_dict[metapath]
        else:
            G = graph
            #logger.info("build_corpus with metapath: %s", metapath)
            walks = G.build_corpus(num_walks, path_length, metapath)
            walks = [list(map(lambda x : str(x), walk)) for walk in walks]
            self.path_dict[metapath] = walks

        #logger.info("train model.")
        model.window = window
        if num_iter:
            model.iter = num_iter
        update = True if model.wv.vocab else False
        model.build_vocab(walks, update=update)
        model.train(walks,total_examples=model.corpus_count,epochs=model.iter)
        self.model = model

    def eval_sim(self, x, y):
        if not hasattr(self, 'model'):
            #logger.warning("no model.")
            return
        model = self.model

        if x not in model.wv.vocab or y not in model.wv.vocab:
            rst = -1
        else:
            rst = model.wv.similarity(x,y)   #Cosine similarity
        return rst


    def get_emb_df(self):
        model = self.model
        df = pd.DataFrame(columns=['node', 'vector'])
        for v in model.wv.vocab:
            df = df.append({'node': v, 'vector': model.wv[v]}, ignore_index=True)
        return df





paths = [('gene','gene','disease'),
        ('gene','disease','disease'),
        ('gene','gene','disease','disease'),
        ('gene','disease','gene','disease'),
        ('gene','miRNA','disease'),
        ('gene','gene','miRNA','disease'),
        ('gene','miRNA','miRNA','disease'),
        ('gene','miRNA','disease','disease')]

#[2]0.91426496319,0.949650159209,0.941581453727,0.966899104683,0.971991037132





def train(filepath, rep_size,selected_paths_idx):

    m = Meta2Vec()

    # data format "node1,type1,node2,type2,score"
    m.load_edges(filepath)

    m.init_model(rep_size)
    if not selected_paths_idx:
        m.train_model(10,10,5,None, num_iter=1, rewalk=True)
    else:
        selected_paths = [paths[i] for i in selected_paths_idx]
        for path in selected_paths:
            m.train_model(10,len(path),5,path, num_iter=1, rewalk=True)
    #logger.info(h.eval_data.groupby('label').apply(lambda x: x.score.mean()))
    #logger.info(h.eval_data.apply(lambda x: x.node1 in h.model.vocab and x.node2 in h.model.vocab, axis=1).value_counts())

    emb_df=m.get_emb_df()
    return emb_df

if __name__== "__main__":
    filepath="D://dmg_small.csv"
    selected_paths_idx = [0]
    rep_size=128
    df = train(filepath, rep_size,selected_paths_idx)
    res_file_name="D://dmg_res.csv" #节点及其对应向量csv文件
    df.to_csv(res_file_name,index=False)

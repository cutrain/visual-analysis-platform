"""
参数说明：graph为传入的带权图（有weight,如果没有请在建图时设置为1）；
rep_size是生成向量的维度，默认128；batch_size默认1000；
epoch默认100，选择loss最小的结果保存；
negtive_ratio为负样本数目，默认为5，一般无需修改；
order=1一阶相似度(first-order),=2二阶相似度（second-order)，默认为3(first-order+second-order)；
"""


import random
import math
import numpy as np
import pandas as pd
import tensorflow as tf
import networkx as nx



class _LINE(object):

    def __init__(self, graph, rep_size=128, batch_size=1000, negative_ratio=5, order=3):
        self.cur_epoch = 0
        self.order = order
        self.g = graph
        self.node_size = graph.G.number_of_nodes()
        self.rep_size = rep_size
        self.batch_size = batch_size
        self.negative_ratio = negative_ratio

        self.gen_sampling_table()
        self.sess = tf.Session()
        cur_seed = random.getrandbits(32)
        #tf.reset_default_graph()
        initializer = tf.contrib.layers.xavier_initializer(
            uniform=False, seed=cur_seed)
        with tf.variable_scope("model", reuse=None, initializer=initializer):
            self.build_graph()
        self.sess.run(tf.global_variables_initializer())


    def build_graph(self):
        self.h = tf.placeholder(tf.int32, [None])
        self.t = tf.placeholder(tf.int32, [None])
        self.sign = tf.placeholder(tf.float32, [None])

        cur_seed = random.getrandbits(32)
        self.embeddings = tf.get_variable(name="embeddings"+str(self.order), shape=[
                                          self.node_size, self.rep_size], initializer=tf.contrib.layers.xavier_initializer(uniform=False, seed=cur_seed))
        self.context_embeddings = tf.get_variable(name="context_embeddings"+str(self.order), shape=[
                                                  self.node_size, self.rep_size], initializer=tf.contrib.layers.xavier_initializer(uniform=False, seed=cur_seed))
        # self.h_e = tf.nn.l2_normalize(tf.nn.embedding_lookup(self.embeddings, self.h), 1)
        # self.t_e = tf.nn.l2_normalize(tf.nn.embedding_lookup(self.embeddings, self.t), 1)
        # self.t_e_context = tf.nn.l2_normalize(tf.nn.embedding_lookup(self.context_embeddings, self.t), 1)
        self.h_e = tf.nn.embedding_lookup(self.embeddings, self.h)
        self.t_e = tf.nn.embedding_lookup(self.embeddings, self.t)
        self.t_e_context = tf.nn.embedding_lookup(
            self.context_embeddings, self.t)
        self.second_loss = -tf.reduce_mean(tf.log_sigmoid(
            self.sign*tf.reduce_sum(tf.multiply(self.h_e, self.t_e_context), axis=1)))
        self.first_loss = -tf.reduce_mean(tf.log_sigmoid(
            self.sign*tf.reduce_sum(tf.multiply(self.h_e, self.t_e), axis=1)))
        if self.order == 1:
            self.loss = self.first_loss
        else:
            self.loss = self.second_loss
        optimizer = tf.train.AdamOptimizer(0.001)
        self.train_op = optimizer.minimize(self.loss)

    def train_one_epoch(self):
        sum_loss = 0.0
        batches = self.batch_iter()
        batch_id = 0
        for batch in batches:
            h, t, sign = batch
            feed_dict = {
                self.h: h,
                self.t: t,
                self.sign: sign,
            }
            _, cur_loss = self.sess.run([self.train_op, self.loss], feed_dict)
            sum_loss += cur_loss
            batch_id += 1
        #print('epoch:{} sum of loss:{!s}'.format(self.cur_epoch, sum_loss))
        self.cur_epoch += 1
        return sum_loss

    def batch_iter(self):
        look_up = self.g.look_up_dict

        table_size = 1e8
        numNodes = self.node_size

        edges = [(look_up[x[0]], look_up[x[1]]) for x in self.g.G.edges()]

        data_size = self.g.G.number_of_edges()
        edge_set = set([x[0]*numNodes+x[1] for x in edges])
        shuffle_indices = np.random.permutation(np.arange(data_size))

        # positive or negative mod
        mod = 0
        mod_size = 1 + self.negative_ratio
        h = []
        t = []
        sign = 0

        start_index = 0
        end_index = min(start_index+self.batch_size, data_size)
        while start_index < data_size:
            if mod == 0:
                sign = 1.
                h = []
                t = []
                for i in range(start_index, end_index):
                    if not random.random() < self.edge_prob[shuffle_indices[i]]:
                        shuffle_indices[i] = self.edge_alias[shuffle_indices[i]]
                    cur_h = edges[shuffle_indices[i]][0]
                    cur_t = edges[shuffle_indices[i]][1]
                    h.append(cur_h)
                    t.append(cur_t)
            else:
                sign = -1.
                t = []
                for i in range(len(h)):
                    t.append(
                        self.sampling_table[random.randint(0, table_size-1)])

            yield h, t, [sign]
            mod += 1
            mod %= mod_size
            if mod == 0:
                start_index = end_index
                end_index = min(start_index+self.batch_size, data_size)

    def gen_sampling_table(self):
        table_size = 1e8
        power = 0.75
        numNodes = self.node_size

        #print("Pre-procesing for non-uniform negative sampling!")
        node_degree = np.zeros(numNodes)  # out degree

        look_up = self.g.look_up_dict
        for edge in self.g.G.edges():
            node_degree[look_up[edge[0]]
                        ] += self.g.G[edge[0]][edge[1]]["weight"]

        norm = sum([math.pow(node_degree[i], power) for i in range(numNodes)])

        self.sampling_table = np.zeros(int(table_size), dtype=np.uint32)

        p = 0
        i = 0
        for j in range(numNodes):
            p += float(math.pow(node_degree[j], power)) / norm
            while i < table_size and float(i) / table_size < p:
                if i % 100000 == 0:
                    print(i, table_size, float(i) / table_size, p, j, numNodes)
                self.sampling_table[i] = j
                i += 1

        data_size = self.g.G.number_of_edges()
        self.edge_alias = np.zeros(data_size, dtype=np.int32)
        self.edge_prob = np.zeros(data_size, dtype=np.float32)
        large_block = np.zeros(data_size, dtype=np.int32)
        small_block = np.zeros(data_size, dtype=np.int32)

        total_sum = sum([self.g.G[edge[0]][edge[1]]["weight"]
                         for edge in self.g.G.edges()])
        norm_prob = [self.g.G[edge[0]][edge[1]]["weight"] *
                     data_size/total_sum for edge in self.g.G.edges()]
        num_small_block = 0
        num_large_block = 0
        cur_small_block = 0
        cur_large_block = 0
        for k in range(data_size-1, -1, -1):
            if norm_prob[k] < 1:
                small_block[num_small_block] = k
                num_small_block += 1
            else:
                large_block[num_large_block] = k
                num_large_block += 1
        while num_small_block and num_large_block:
            num_small_block -= 1
            cur_small_block = small_block[num_small_block]
            num_large_block -= 1
            cur_large_block = large_block[num_large_block]
            self.edge_prob[cur_small_block] = norm_prob[cur_small_block]
            self.edge_alias[cur_small_block] = cur_large_block
            norm_prob[cur_large_block] = norm_prob[cur_large_block] + norm_prob[cur_small_block] - 1
            if norm_prob[cur_large_block] < 1:
                small_block[num_small_block] = cur_large_block
                num_small_block += 1
            else:
                large_block[num_large_block] = cur_large_block
                num_large_block += 1

        while num_large_block:
            num_large_block -= 1
            self.edge_prob[large_block[num_large_block]] = 1
        while num_small_block:
            num_small_block -= 1
            self.edge_prob[small_block[num_small_block]] = 1

    def get_embeddings(self):
        vectors = {}
        embeddings = self.embeddings.eval(session=self.sess)
        # embeddings = self.sess.run(tf.nn.l2_normalize(self.embeddings.eval(session=self.sess), 1))
        look_back = self.g.look_back_list
        for i, embedding in enumerate(embeddings):
            vectors[look_back[i]] = embedding
        return vectors


class LINE(object):
    def __init__(self, graph, rep_size=128, batch_size=1000, epoch=100, negative_ratio=5, order=3, auto_save=True):
        self.rep_size = rep_size
        self.order = order
        self.best_result = 1e9
        self.best_ite=0
        self.vectors = {}
        if order == 3:
            self.model1 = _LINE(graph, int(rep_size/2), batch_size,
                                negative_ratio, order=1)
            self.model2 = _LINE(graph,int(rep_size/2), batch_size,
                                negative_ratio, order=2)
            for i in range(epoch):
                loss1=self.model1.train_one_epoch()
                loss2=self.model2.train_one_epoch()
                loss=loss1+loss2
                self.get_embeddings()
                # pos_test=gen_pos(df_test, self.vectors)
                # neg_test=gen_neg(pos_test,df_train,df_GD,df_MD,is_test_GD,self.vectors)
                # test_data=gen_test(pos_test, neg_test)
                # result=auc_score(test_data)
                if loss < self.best_result:
                        self.best_result = loss
                        self.best_ite=i
                        if auto_save:
                            self.best_vector = self.vectors
            self.model1.sess.close()
            self.model2.sess.close()

        else:
            self.model = _LINE(graph, rep_size, batch_size,
                               negative_ratio, order=self.order)
            for i in range(epoch):
                loss=self.model.train_one_epoch()
                self.get_embeddings()
                if loss<self.best_result:
                    self.best_result=loss
                    self.best_ite = i
                    if auto_save:
                        self.best_vector=self.vectors
            self.model.sess.close()

        if auto_save:
            self.vectors = self.best_vector


    def get_embeddings(self):
        self.last_vectors = self.vectors
        self.vectors = {}
        if self.order == 3:
            vectors1 = self.model1.get_embeddings()
            vectors2 = self.model2.get_embeddings()
            for node in vectors1.keys():
                self.vectors[node] = np.append(vectors1[node], vectors2[node])
        else:
            self.vectors = self.model.get_embeddings()

    def save_embeddings(self, filename):
        df=pd.DataFrame(columns=['node','vector'])
        for node, vec in self.vectors.items():
            df=df.append({'node': node, 'vector': vec}, ignore_index=True)
        df.to_csv(filename,index=False)


class Graph(object):
    def __init__(self):
        self.G = None
        self.look_up_dict = {}
        self.look_back_list = []
        self.node_size = 0

    def encode_node(self):
        look_up = self.look_up_dict
        look_back = self.look_back_list
        for node in self.G.nodes():
            look_up[node] = self.node_size
            look_back.append(node)
            self.node_size += 1
            # self.G.nodes[node]['status'] = ''

    def read_g(self, g):
        self.G = g
        self.encode_node()

    def read_graph(self,df):
        G = nx.Graph()
        def load_single_entry(x):
            G.add_node(x['node1'], type=x['node1_type'])
            G.add_node(x['node2'], type=x['node2_type'])
            G.add_edge(x['node1'], x['node2'], weight=float(x['weight']))
        df.apply(load_single_entry, axis=1)
        self.G=G
        self.encode_node()










if __name__ == "__main__":
    input_csv="~/project/visual-analysis-platform/data/GD_human.csv"#文件路径名称
    graph_df = pd.read_csv(input_csv, names=['node1', 'node1_type', 'node2', 'node2_type', 'weight'],
                          dtype={'node1': str, 'node2': str, 'weight': float})
    g = Graph()
    g.read_graph(graph_df)
    model = LINE(g,epoch=1,rep_size=128, order=3)
    model.save_embeddings("./test.csv") #filename为要写入的文件名及路径

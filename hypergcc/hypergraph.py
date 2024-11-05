'''
MIT License

Copyright (c) 2021 Kazuki Nakajima
Copyright (c) 2024 Rikuya Miyashita
Copyright (c) 2024 Shiori Hironaka

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Implemented the three clustering coefficients to the original code (https://github.com/kazuibasou/hyper-dk-series/blob/main/py/hypergraph.py)
中嶋さんのハイパーグラフのクラス(https://github.com/kazuibasou/hyper-dk-series/tree/main/py)を基に3つのクラスタ係数を計算する関数などを追加した．
'''
import math
import pathlib
import itertools

import logging
logger = logging.getLogger(__name__)


def read_hypergraph_from_file(f_nverts, f_hyperedges):
    V = []
    E = []
    elist = {}

    # original
    # c = 0
    # e_i = 0
    # for line1 in lines1:
    #     nv = int(line1[:-1].split(" ")[0])
    #
    #     e = []
    #     for i in range(0, nv):
    #         v = int(lines2[c+i][:-1])
    #         e.append(v)
    #
    #     E.append(e)
    #     for v in e:
    #         if v not in V:
    #             V.append(v)
    #             elist[v] = []
    #         elist[v].append(e_i)
    #     c += nv
    #     e_i += 1

    # rewrite
    c = 0
    e_i = 0
    for e_i, line1 in enumerate(f_nverts):
        nv = int(line1.rstrip())
        e = [int(next(f_hyperedges).rstrip()) for _ in range(nv)]
        E.append(e)

        for v in e:
            if v not in V:
                V.append(v)
                elist[v] = []
            elist[v].append(e_i)
        c += nv
    return V, E, elist


class HyperGraph():
    def __init__(self, datadir_path):
        # hypergraph datasetがあるディレクトリ
        self.datadir = pathlib.Path(datadir_path)

        self.V: list[int] = []  # A list of nodes
        self.E: list[list[int]] = []  # A list of hyperedges
        self.elist: dict[int, list[int]] = {}  # A dictionary of lists of indices in the list E of hyperedges to which each node belongs

        # Example
        # V = [1, 2, 3, 4, 5]
        # E = [[1, 2], [2, 3], [1, 2, 3], [1, 2, 3, 4], [1, 2, 3, 4, 5]]
        # elist = {1: [0, 2, 3, 4], 2: [0, 1, 2, 3, 4], 3: [1, 2, 3, 4], 4: [3, 4], 5: [4]}
        # In this example, elist[1] = [0, 2, 3, 4] implies that node 1 belongs to hyperedges E[0], E[2], E[3], and E[4].

    def construct_hypergraph(self, V: list[int], E: list[list[int]]):
        '''Construct a hypergraph from a set of nodes V and a set of hyperedges E.'''
        self.V = list(V)
        self.E = list(E)
        self.elist = {v: [] for v in self.V}

        for i in range(0, len(E)):
            for v in E[i]:
                self.elist[v].append(i)

        return

    def read_hypergraph(self, hypergraph_name):
        '''Read hypergraph named hypergraph_name.

        The corresponding files to read must be in the self.datadir directory
        '''
        f1_path = self.datadir / f'{hypergraph_name}_nverts.txt'
        f2_path = self.datadir / f'{hypergraph_name}_hyperedges.txt'

        with open(f1_path, 'r') as f1, open(f2_path, 'r') as f2:
            V, E, elist = read_hypergraph_from_file(f1, f2)

        self.V = V
        self.E = E
        self.elist = elist

        logger.info('Hypergraph named ' + str(hypergraph_name) + ' was read.')
        logger.info("Number of nodes: %d", len(self.V))
        logger.info("Number of hyperedges: %d", len(self.E))


    def add_node_to_hyperedge(self, v, e_i):
        '''Add node v to hyperedge E[e_i]'''
        if v not in self.elist:
            msg = "Error: Given node is not found."
            logger.error(msg)
            raise ValueError(msg)
        if e_i < 0 or len(self.E) <= e_i:
            msg = "Error: Given hyperedge is not found."
            logger.error(msg)
            raise ValueError(msg)

        self.E[e_i].append(v)
        self.elist[v].append(e_i)


    def remove_node_from_hyperedge(self, v, e_i):
        '''Remove node v from hyperedge E[e_i]'''
        if v not in self.elist:
            msg = "Error: Given node is not found."
            logger.error(msg)
            raise ValueError(msg)
        if e_i < 0 or len(self.E) <= e_i:
            msg = "Error: Given hyperedge is not found."
            logger.error(msg)
            raise ValueError(msg)

        if e_i not in self.elist[v]:
            msg = "Error: Given node is not included in the given hyperedge."
            logger.error(msg)
            raise ValueError(msg)

        if v not in self.E[e_i]:
            msg = "Error: Given node does not belong to the given hyperedge."
            logger.error(msg)
            raise ValueError(msg)

        self.elist[v].remove(e_i)
        self.E[e_i].remove(v)


    def node_degree(self):
        '''Calculate the degree of each node (i.e., the number of hyperedges to which each node belongs).'''
        nd = {}
        for v in self.V:
            nd[v] = int(len(self.elist[v]))

        return nd

    def num_jnt_node_deg(self):
        '''Calculate the number of hyperedges that nodes with degree k and nodes with degree k' share.'''
        node_degrees = set()
        for v in self.V:
            k = int(len(self.elist[v]))
            node_degrees.add(k)

        jnd = {k1: {k2: 0 for k2 in node_degrees} for k1 in node_degrees}

        for e in self.E:
            s = int(len(e))
            for i in range(0, s-1):
                u = e[i]
                k1 = int(len(self.elist[u]))
                for j in range(i+1, s):
                    v = e[j]
                    k2 = int(len(self.elist[v]))
                    jnd[k1][k2] += 1
                    jnd[k2][k1] += 1

        return jnd

    def neighbors(self, v: int):
        neighbors: set[int] = set()
        for i in self.elist[v]:
            neighbors |= set(self.E[i])
        neighbors -= set((v,))
        return neighbors


    # 3種のクラスタ係数の計算を追加

    def node_clustering_coefficient_opsahl(self):
        '''Calculate Opsahl's clustering coefficients'''

        # 各ノード v と少なくとも1本のハイパーエッジを共有するノードの集合を作成
        nlist_set = {k: set() for k in self.V}
        for v in self.V:
            for e in self.elist[v]:
                nlist_set[v] = nlist_set[v] | set(self.E[e])
                nlist_set[v].discard(v)

        # 各ノードv1, v2の共有するハイパーエッジを保存
        common_elist_set = {k: {k1: set() for k1 in nlist_set[k]} for k in self.V}
        for v1 in self.V:
            set_elist_v1 = set(self.elist[v1])
            for v2 in nlist_set[v1]:
                common_elist_set[v1][v2] = set_elist_v1 & set(self.elist[v2])

        c_opsahl = {v: 0.0 for v in self.V}
        numer = {v: 0.0 for v in self.V}
        denom = {v: 0.0 for v in self.V} 

        for v in self.V:
            for (e1, e2) in itertools.combinations(self.elist[v], 2):
                if e1 == e2:
                    continue
                for v1 in self.E[e1]:
                    if v1 == v:
                        continue
                    for v2 in self.E[e2]:
                        if v2 == v or v2 == v1:
                            continue

                        denom[v] += 1
                        if v2 not in common_elist_set[v1]:
                            continue
                        if len(common_elist_set[v1][v2] - {e1} - {e2}) > 0:
                            numer[v] += 1

            if denom[v] != 0:
                c_opsahl[v] = numer[v] / denom[v]

        return c_opsahl

    def node_clustering_coefficient_opsahl_by_fraction(self):
        '''Calculate Opsahl's clustering coefficients with denominators and numerators
        各ノードのクラスタ係数を求め，分子，分母と共に出力．'''

        # クラスタ係数と，その分子，分母を辞書として定義
        cc = {v: 0.0 for v in self.V}
        cc_numer = {v: 0.0 for v in self.V}
        cc_denom = {v: 0.0 for v in self.V} 

        for v in self.V:
            for (e_1, e_2) in itertools.combinations(self.elist[v], 2):
                if e_1 == e_2:
                    continue
                for v1 in self.E[e_1]:
                    if v1 == v:
                        continue
                    set_elist_v1 = set(self.elist[v1])
                    for v2 in self.E[e_2]:
                        if v2 == v or v2 == v1:
                            continue
                        cc_denom[v] += 1
                        if len(set_elist_v1 & set(self.elist[v2]) - {e_1} - {e_2}) > 0:
                            cc_numer[v] += 1

            # 分母が0でなければ，除算によりクラスタ係数を計算
            if cc_denom[v] != 0:
                cc[v] = cc_numer[v] / cc_denom[v] 

        return cc, cc_numer, cc_denom

    def node_clustering_coefficient_zhou(self):
        '''Calculate Zhou's clustering coefficients'''

        c_zhou = {v: 0.0 for v in self.V} 
        numer = {v: 0.0 for v in self.V}
        denom = {v: 0.0 for v in self.V}

        nlist_set = {k: set() for k in self.V} # vの隣接ノードの集合
        for v in self.V:
            for e in self.elist[v]:
                nlist_set[v] = nlist_set[v] | set(self.E[e])
            nlist_set[v].discard(v)

        for v in self.V:

            if len(self.elist[v]) <= 1: # d(v) <= 1 ならば0のまま
                continue

            # denom[v] = len(edge_pairs)
            denom[v] = math.comb(len(self.elist[v]), 2)

            for pair in itertools.combinations(self.elist[v], 2):

                e1 = set(self.E[pair[0]])
                e2 = set(self.E[pair[1]])
                d12 = e1 - e2
                d21 = e2 - e1
                if len(d12)==0 or len(d21)==0:
                    continue
                eo_num1 = 0
                for v21 in d21:
                    for v12 in d12:
                        if v21 in nlist_set[v12]:
                            eo_num1 += 1
                            break
                eo_num2 = 0
                for v12 in d12:
                    for v21 in d21:
                        if v12 in nlist_set[v21]:
                            eo_num2 += 1
                            break
                numer[v] += (eo_num1+eo_num2) / (len(d12) + len(d21))


            if denom[v] != 0:
                c_zhou[v] = numer[v] / denom[v] 

        return c_zhou

    def node_clustering_coefficient_proposed(self):
        '''Calculate the proposed clustering coefficients'''

        c_proposed = {v: 0.0 for v in self.V} 
        numer = {v: 0.0 for v in self.V}
        denom = {v: 0.0 for v in self.V}

        nlist_set = {k: set() for k in self.V} # vの隣接ノードの集合
        for v in self.V:
            for e in self.elist[v]:
                nlist_set[v] = nlist_set[v] | set(self.E[e])
            nlist_set[v].discard(v)

        weight = {k: {k1: 0.0 for k1 in nlist_set[k]} for k in self.V} # ノードv1, v2間の重み
        for v1 in self.V:
            for v2 in nlist_set[v1]:
                common_hyperedges = set(self.elist[v1]) & set(self.elist[v2])
                emin = len(self.V)
                for e in common_hyperedges:
                    emin = min(emin, len(self.E[e]))
                weight[v1][v2] = 1 / (emin - 1)

        for v in self.V:
            node_pairs = itertools.combinations(nlist_set[v], 2)
            for (v1, v2) in node_pairs:
                denom[v] +=  weight[v][v1] * weight[v][v2]
                if v2 not in weight[v1]:
                    continue
                numer[v] += weight[v][v1] * weight[v][v2] * weight[v1][v2]

            if denom[v] != 0:
                c_proposed[v] = numer[v] / denom[v] 

        return c_proposed

    def node_clustering_coefficient_on_projected_graph(self):
        '''Calculate clustering coefficients on projected undirected simple graph'''

        logger.info('Converting hypergraph into simple graph...')
        import networkx as nx
        simple_graph = nx.Graph()
        simple_graph.add_nodes_from(self.V)
        for he in self.E:
            simple_graph.add_edges_from(itertools.combinations(he, 2))

        logger.info('Computing clustering coefficients...')
        out = nx.clustering(simple_graph)
        return out

    def hyperedge_size(self):
        '''Calculate the size of each hyperedge (i.e., the number of nodes that belong to each hyperedge).'''

        hs = {}

        for e_i in range(0, len(self.E)):
            hs[e_i] = len(self.E[e_i])

        return hs

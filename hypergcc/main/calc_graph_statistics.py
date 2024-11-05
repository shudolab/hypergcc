'''
Calculate dataset statistics
- Number of nodes
- number of hyperedges
- number of edges in the corresponding bipartite graph
- average degree of the nodes
- average size of the hyperedges
'''
import numpy as np
from hypergcc.hypergraph import HyperGraph


def main(args):
    # ハイパーグラフのデータを読み込む
    G = HyperGraph(args.dataset_dir)
    G.read_hypergraph(args.dataset)

    num_nodes = len(G.V)
    num_hyperedges = len(G.E)
    num_edges_bi = sum([len(el) for el in G.elist.values()])
    avg_degree = np.mean(list(G.node_degree().values()))
    avg_hyperedges = np.mean([len(e) for e in G.E])

    print(args.dataset, num_nodes, num_hyperedges, num_edges_bi, avg_degree, avg_hyperedges, sep='\t')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_dir')
    parser.add_argument('dataset')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)

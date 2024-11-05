'''
Calculate features for each node
- degree (number of hyperedges to which the node belongs)
- number of neighbors (number of unique nodes that belongs to the same hyperedge with)
  { v | e \\in E, u \\in e, v \\in e, u \\ne v }
- average size (cardinality) of hyperedges that the node belongs to
'''
import numpy as np
from hypergcc.hypergraph import HyperGraph


def main(args):
    # ハイパーグラフのデータを読み込む
    G = HyperGraph(args.dataset_dir)
    G.read_hypergraph(args.dataset)

    degrees = G.node_degree()

    neighbors = {u: len(G.neighbors(u)) for u in G.V}

    avg_hyperedges = {u: np.mean([len(G.E[i]) for i in G.elist[u]]) for u in G.V}

    for u in G.V:
        print(u, degrees[u], neighbors[u], avg_hyperedges[u], sep='\t')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_dir')
    parser.add_argument('dataset')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)

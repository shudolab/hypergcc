# Code is from https://github.com/FraLotito/higher-order-motifs/
# Under MIT License

from hypergcc.motifs import loaders
from hypergcc.hypergraph import HyperGraph
from hypergcc.motifs.motifs2 import motifs_order_3
from hypergcc.motifs.motifs import count_motifs


def count_motifs_order3(G):
    hedges = loaders.load_from_hyperedgelist(3, G.E)
    # hedges = loaders.load_high_school(3)
    # hedges = loaders.load_facebook_hs()

    # result = count_motifs(hedges, 3, -1)
    result = motifs_order_3(hedges, -1)
    return result


def main(args):
    # ハイパーグラフのデータを読み込む
    G = HyperGraph(args.dataset_dir)
    G.read_hypergraph(args.dataset)
    motifs = count_motifs_order3(G)

    for k, v in motifs:
        print(k, v, sep='\t')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_dir')
    parser.add_argument('dataset')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)

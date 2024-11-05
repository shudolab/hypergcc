'''
ローカルクラスタリング係数を計算する
'''

import sys
from hypergcc.hypergraph import HyperGraph

import logging
logging.basicConfig(level=logging.DEBUG, format='{asctime} [{levelname:.4}] {name}: {message}', style='{')
logger = logging.getLogger(__name__)

IMPLEMENTED_METHODS = ['opsahl', 'zhou', 'proposed', 'simple']


def main(args):
    # ハイパーグラフのデータを読み込む
    G = HyperGraph(args.dataset_dir)
    G.read_hypergraph(args.dataset)

    # 各定義によるクラスタ係数を計算
    logger.info('Calculating clustering coefficient using %s method ...', args.method)
    match args.method:
        case 'opsahl':
            cc, A, B = G.node_clustering_coefficient_opsahl_by_fraction()
        case 'zhou':
            cc = G.node_clustering_coefficient_zhou()
        case 'proposed':
            cc = G.node_clustering_coefficient_proposed()
        case 'simple':
            cc = G.node_clustering_coefficient_on_projected_graph()
        case _:
            sys.exit(1)
    logger.info('done')

    # クラスタ係数を出力
    for node, value in cc.items():
        print(node, value, sep='\t')


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset_dir')
    parser.add_argument('dataset')
    parser.add_argument('method', choices=IMPLEMENTED_METHODS)
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

'''
平均クラスタ係数を求める

calc_averageって名前でもいいくらい
'''
import numpy as np


def main(args):
    cc = [float(line.rstrip().split('\t')[1]) for line in args.cc]
    mean_cc = np.mean(cc)
    print(mean_cc)


def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('cc', type=argparse.FileType('r'))
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    main(args)

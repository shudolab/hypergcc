"""
This file implements the efficient algorithm for motif discovery in hypergraphs.

MIT License

Copyright (c) 2022 Francesco Lotito

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
"""

# from .hypergraph import hypergraph
from .utils import *
from .loaders import *

def motifs_order_3(edges, TOT):
    N = 3
    full, visited = motifs_ho_full(edges, N, TOT)
    standard = motifs_standard(edges, N, TOT, visited)

    res = []
    for i in range(len(full)):
        res.append((full[i][0], max(full[i][1], standard[i][1])))

    return res

def motifs_order_4(edges, TOT):
    N = 4
    full, visited = motifs_ho_full(edges, N, TOT)
    not_full, visited = motifs_ho_not_full(edges, N, TOT, visited)
    standard = motifs_standard(edges, N, TOT, visited)

    res = []
    for i in range(len(full)):
        res.append((full[i][0], max([full[i][1], not_full[i][1], standard[i][1]])))

    return res

# N = 3
#
# edges = load_high_school(N)
#
# output = {}
#
# if N == 3:
#     output['motifs'] = motifs_order_3(edges, -1)
# elif N == 4:
#     output['motifs'] = motifs_order_4(edges, -1)
#
# print(output['motifs'])
#
# STEPS = len(edges)*10
# ROUNDS = 10
#
# results = []
#
# for i in range(ROUNDS):
#     e1 = hypergraph(edges)
#     e1.MH(label='stub', n_steps=STEPS)
#     if N == 3:
#         m1 = motifs_order_3(e1.C, i)
#     elif N == 4:
#         m1 = motifs_order_4(e1.C, i)
#     results.append(m1)
#
# output['config_model'] = results
#
# delta = diff_sum(output['motifs'], output['config_model'])
# norm_delta = norm_vector(delta)
#
# print(norm_delta)

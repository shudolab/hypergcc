from pathlib import Path

# Dataset directory path
DATASET_DIR = Path('data')

# Dataset names
DATASETS = ['DavisClub', 'NDCc', 'cps', 'eE']
METHODS = ['opsahl', 'zhou', 'proposed', 'simple']

# Output base directory
OUTPUT_DIR = Path('output')


rule all:
    input:
        OUTPUT_DIR / 'mean_cc.tsv',
        OUTPUT_DIR / 'stats' / 'dataset_stats.tsv',
        expand(OUTPUT_DIR / 'motifs' / 'motifs_{dataset}.tsv', dataset=DATASETS),
        expand(OUTPUT_DIR / 'stats' / 'nodes' / '{dataset}.tsv', dataset=DATASETS),


rule calc_clustering_coefficients:
    input:
        datasetdir=DATASET_DIR,
        hyperedges=DATASET_DIR / '{dataset}_hyperedges.txt',
        nverts=DATASET_DIR / '{dataset}_nverts.txt',
    output:
        OUTPUT_DIR / 'node-cc' / '{dataset}' / 'ncc_{method}.tsv'
    shell:
        '''
        python -m hypergcc.main.calc_ncc {input.datasetdir} {wildcards.dataset} {wildcards.method} > {output}
        '''

rule calc_mean_cc:
    input:
        OUTPUT_DIR / 'node-cc' / '{dataset}' / 'ncc_{method}.tsv'
    output:
        OUTPUT_DIR / 'mean-cc' / 'meancc_{dataset}_{method}.tsv'
    shell:
        '''
        echo -ne '{wildcards.dataset}\\t{wildcards.method}\\t' > {output}
        python -m hypergcc.main.calc_cc {input} >> {output}
        '''

rule gather_mean_cc:
    input:
        expand(OUTPUT_DIR / 'mean-cc' / 'meancc_{dataset}_{method}.tsv', dataset=DATASETS, method=METHODS)
    output:
        OUTPUT_DIR / 'mean_cc.tsv'
    shell:
        '''
        cat {input} > {output}
        '''

rule calc_dataset_statistics:
    input:
        datasetdir=DATASET_DIR,
        hyperedges=DATASET_DIR / '{dataset}_hyperedges.txt',
        nverts=DATASET_DIR / '{dataset}_nverts.txt',
    output:
        OUTPUT_DIR / 'stats' / 'datasets' / '{dataset}.tsv'
    shell:
        'python -m hypergcc.main.calc_graph_statistics {input.datasetdir} {wildcards.dataset} > {output}'

rule gather_dataset_statistics:
    input:
        expand(OUTPUT_DIR / 'stats' / 'datasets' / '{dataset}.tsv', dataset=DATASETS)
    output:
        OUTPUT_DIR / 'stats' / 'dataset_stats.tsv'
    shell:
        'cat {input} > {output}'

rule count_motifs_order3:
    input:
        datasetdir=DATASET_DIR,
        hyperedges=DATASET_DIR / '{dataset}_hyperedges.txt',
        nverts=DATASET_DIR / '{dataset}_nverts.txt',
    output:
        OUTPUT_DIR / 'motifs' / 'motifs_{dataset}.tsv'
    shell:
        '''
        python -m hypergcc.main.count_motifs {input.datasetdir} {wildcards.dataset} > {output}
        '''


rule calc_node_degrees:
    input:
        datasetdir=DATASET_DIR,
        hyperedges=DATASET_DIR / '{dataset}_hyperedges.txt',
        nverts=DATASET_DIR / '{dataset}_nverts.txt',
    output:
        OUTPUT_DIR / 'stats' / 'nodes' / '{dataset}.tsv'
    shell:
        '''
        python -m hypergcc.main.calc_degrees {input.datasetdir} {wildcards.dataset} > {output}
        '''

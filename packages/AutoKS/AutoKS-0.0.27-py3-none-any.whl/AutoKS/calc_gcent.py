#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx


def calc_gcent(G, detailed=False):
    """
    calculate the Graph Centrality (gcent) of a graph.

    see:
    Clariana, R. B., Rysavy, M. D., & Taricani, E. (2015). Text signals
    influence team artifacts. Educational Technology Research and Development,
    63(1), 35-52.

    :param G: a NeyworkX graph.
    :param detailed: show detailed information of calculation or not. Default is
    False.
    :return: a number of gcent.
    """
    # get adjacency matrix from a graph
    array = nx.to_numpy_array(G)

    n = G.number_of_nodes()

    node_degree = np.sum(array, axis=0)

    # ncent=node_degree/(n−1)
    ncent = node_degree/(n - 1)

    MAXncent = np.max(ncent)
    # gcent=Σ{[max(ncent)−ncent(i)]/(n−2)}
    gcent = np.sum((MAXncent - ncent)/(n - 2))

    if detailed:
        print('\nadjacency matrix:\n', array)
        print('n:', n)
        print('node_degree:', node_degree)
        print('ncent:', ncent)
        print('gcent:', gcent)

    return gcent

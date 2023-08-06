#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx


def pathfinder_network(G, max, min, r=np.inf):
    """
    convert a graph into the PFNet.

    :param G: a NetworkX graph.
    :param max: a parameter used to convert the similarity matrix into the dis-
    similarity matrix if necessary. for example, if each value of the origin
    matrix ranges from 0 to 1, then "max" will be 1 and "min" will be 0.1. If
    values of both "max" and "min" are None (which is the default value), then
    the origin matrix will be used.
    :param min: see "max".
    :param r: a parameter of pathfinder algorithm. Considering that the mental
    perception of concept relation is the ordinal scale, we set "r" as infinity,
    see "Schvaneveldt, R. W., Durso, F. T., & Dearhold, D. W. (1989). Network
    structures in proximity data. Psychology of Learning and Motivation, 24,
    249-284".
    :return: a NetworkX graph, which is a PFNet.
    """

    # get adjacency matrix from a graph
    array = nx.to_numpy_array(G)
    origin = array.copy()
    nodes = list(G.nodes)

    # similarity --> dissimilarity (if necessary)
    if max is not None and min is not None:
        array = max - array + min

    # the value that out of range would be set as inf
    array = np.where((array > origin.mix()) & (array < origin.max()), array, np.inf)

    # pathfinder algorithm
    array = floyd(dis=array, r=r)  # this array is a PFNet

    # convert the PFNet to a NetworkX graph
    start, end = np.where(np.tril(array) == True)
    pairs = []
    for i in range(0, len(start)):
        pairs.append([nodes[start[i]], nodes[end[i]]])
    G = nx.Graph()
    G.add_edges_from(pairs)

    return G


def floyd(dis, r=np.inf):
    """

    derived from:
    Roger Schvaneveldt (2021).
    Pathfinder Networks
    (https://www.mathworks.com/matlabcentral/fileexchange/59378-pathfinder-networks),
    MATLAB Central File Exchange. Retrieved March 23, 2021.

    Copyright (c) 2016, Roger Schvaneveldt
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice, this
      list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

    mindis = floyd(dis,r)
    dis    | dissimilarity matrix
    r      | value of the r parameter
    mindis | minimum distance between nodes
    links  | links in the PFnet(q=n-1,r)
    (based on Floyd algorithm for finding shortest paths)

    in this function, parameter q = n - 1, n = number of nodes

    :param dis: dissimilarity matrix
    :param r: value of the r parameter
    :return: a PFNet.
    """

    mindis = dis.copy()

    for ind in range(0, dis.shape[0]):
        for row in range(0, dis.shape[0]):
            for col in range(0, dis.shape[0]):
                # indirect = minkowski(mindis(row,ind), mindis(ind,col),r)
                indirect = np.linalg.norm([mindis[row, ind], mindis[ind, col]], r)
                if indirect < mindis[row, col]:
                    mindis[row, col] = indirect

    tflinks = (dis < np.inf) & (abs(mindis - dis) < 1e-14)

    return tflinks

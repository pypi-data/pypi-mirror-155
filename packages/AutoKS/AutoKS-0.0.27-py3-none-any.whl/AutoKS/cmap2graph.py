# !/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from os.path import basename
from .pathfinder_network import *
from .read_file import *


def cmap2graph(
        file,
        data_type,
        keyterms=None,
        read_from_file=True,
        encoding='utf-8',
        read_from=0,
        pfnet=False,
        max=None,
        min=None,
        r=np.inf):
    """
    convert the concept map (or proximity/adjacency matrix) into a graph.

    :param file: a list or a file path of a .txt document. Theoretically,
    contents can be written in any language, as long as Python and your computer
    support it. If you try to open a file, then you might have to set a suitable
    encoding form, for example, if contents is written in Chinese, the .txt file
    better save as utf-8 encoding, and should be open as the same encoding too.
    :param data_type: "pair" or "array". For the data type "pair", "file" should
    be a list contained every propositions/edges/links/lines from a concept map,
    e.g.,
    file = [['concept A', 'concept B'], ['concept A', 'concept C'], ...]
    For the data type  "array", "file" should be a n*n proximity/adjacency
    matrix, n = number of key-terms, both row and column represent key-terms and
    value(i, j) represents the relationship of concept(i) and concept(j). Both
    rectangle and triangle matrix are acceptable.
    :param keyterms: a list contained some string variables, each string is one
    key-term. All key-terms should be written in lower case, but upper case is
    also acceptable, as long as value of the parameter "as_lower" have been set
    as False.
    :param read_from_file: if True, then manipulate the "file" parameter as a
    string, if False, then manipulate the "file" parameter as a file path.
    :param encoding: default is "utf-8", which supports most languages, such as
    English, Chinese, Korean, Arabic, etc.
    :param read_from: from which row (line) to read when opening data from a
    file. Noted that the index of the first row (line) is 0.
    :param pfnet: converts the output into a undirected PFNet if set as True.
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
    :return: a NetworkX graph represented the Knowledge Structure network.
    """

    try:
        assert data_type in ['pair', 'array']
    except:
        print('\033[0;31m\nERROR: the value of "data_type" is unrecognized, '
              'it must be either "pair" or "array"!\033[0m')
        exit(1)

    G = nx.Graph()

    if read_from_file:
        G.name = basename(file.split('.')[0])

        # Step 1: read file, each line in the file, add each line into the list
        content = read_file(file, encoding=encoding)
    else:
        content = list(file)

    # Step 2: find data by index (i.e., the parameter 'read_from'), skip the unwanted content
    if type(read_from) == int:
        content = content[read_from:]
    elif type(read_from) in [tuple, list]:
        content = content[read_from[0]:read_from[1]]
    if data_type == 'array':
        # Step 3-1: convert the triangle matrix to a n*n matrix (if necessary)
        # this means a triangle matrix
        # add first row, this is m[0, 0]
        # add elements in each row until the number of elements equal to n
        print(content)
        print('len(content[0]) & len(content[-1])', len(content[0]), len(content[-1]))
        if len(content[0]) != len(content[-1]):
            print('convert it into n*n array')
            content.insert(0, ['0'])
            for i in range(0, len(content)):
                while len(content[i]) != len(content):
                    content[i].append('')

            print('content', content)

            # Step 3-2: add value
            # for each element m[i, j]
            # for each element in the diagonal line
            # for each element in the upper part of the triangle
            for i in range(0, len(content)):
                for j in range(0, len(content)):
                    if i == j:
                        content[i][j] = '0'
                    elif i < j:
                        content[i][j] = content[j][i]

            print('content', content)

        # Step 3-3: convert each value from string to int
        array = np.zeros([len(content), len(content)])

        print('len(array)', len(array))

        print('len(content)', len(content))

        for i in range(0, len(content)):
            for j in range(0, len(content)):

                # print('content[i][j]', content[i][j])

                array[i, j] = int(content[i][j])

                # print('array', array)

        print('array', array)

        # Step 4: calculate PFNet (if necessary)
        if pfnet:
            if max is not None and min is not None:  # similarity --> distances (if necessary)
                array = max - array + min
                # the value that out of range would be set as inf
                array = np.where((array > min) & (array < max), array, np.inf)

            array = floyd(array, r=r)

        # Step 5: convert it to a graph
        start, end = np.where(np.tril(array) == True)
        pairs = []
        for i in range(0, len(start)):
            pairs.append([keyterms[start[i]], keyterms[end[i]]])
        G.add_edges_from(pairs)
    elif data_type == 'pair':
        for pair in content:
            G.add_edge(pair[0], pair[1])

    return G

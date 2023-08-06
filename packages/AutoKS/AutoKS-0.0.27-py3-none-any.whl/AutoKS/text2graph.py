#!/usr/bin/env python
# -*- coding: utf-8 -*-

from re import finditer
import sys
import networkx as nx
from .pathfinder_network import *


def text2graph(
        text,
        keyterms,
        synonym=None,
        read_from_file=True,
        name=None,
        encoding='utf-8',
        as_lower=True,
        pfnet=False,
        max=None,
        min=None,
        r=np.inf
):
    """
    Convert the text into a graph.

    :param text: a string or a file path of a .txt document. Theoretically, contents
    can be written in any language, as long as Python and your computer support
    it. If you try to open a file, then you might have to set a suitable
    encoding form, for example, if contents is written in Chinese, the .txt file
    better save as utf-8 encoding, and should be open as the same encoding too.
    :param keyterms: a list contained some string variables, each string is one
    key-term. All key-terms should be written in lower case, but upper case is
    also acceptable, as long as value of the parameter "as_lower" have been set
    as False.
    :param synonym: a dictionary. Each key is a term form key-terms list, and
    value can be a list contained synonym(s), e.g.,
    synonym={'a':['a1', 'a2'], 'b':['b1']}
    :param read_from_file: if True, then manipulate the "text" parameter as a
    string, if False, then manipulate the "text" parameter as a file path.
    :param encoding: default is "utf-8", which supports most languages, such as
    English, Chinese, Korean, Arabic, etc.
    :param name: name of Graph.
    :param as_lower: convert every character in the text into lower case.
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

    # ERROR information
    if synonym:
        try:
            assert type(synonym) == dict
        except:
            print('\033[0;31m\nERROR: the "synonym" is unrecognized, '
                  'it must be a dict object!\033[0m')
            exit(1)

        try:
            for i in synonym.values():
                assert type(i) == list
        except:
            print('\033[0;31m\nERROR: the "synonym" is unrecognized, '
                  'the value of each key must be a list object!\033[0m')
            exit(1)

    G = nx.Graph()
    # add every nodes from key-terms list into the graph firstly, because some
    # participants' data may miss several key-terms or they only use some.
    for term in keyterms:
        G.add_node(term)

    if name or "//" not in text:
        G.name = name

    if read_from_file:  # so the object 'text' is a filepath
        file_text = ''
        with open(text, 'r', encoding=encoding) as f:
            for line in f.readlines():
                line = line.strip()
                file_text += line
        text = file_text

    # error information
    for i in keyterms:
        for t in keyterms:
            if i != t and i in t and keyterms.index(i) < keyterms.index(t):
                print('\033[0;31m\nERROR!\n'
                      '"{}" comes before "{}" in key terms list!\n'
                      'this might conduct some error, \n'
                      'because term "{}" in the text would be detected as term '
                      '"{}".\n'
                      'please re-order your terms list and insure "{}" after '
                      '"{}".\033[0m'
                      .format(i, t, i, t, i, t))
                sys.exit(1)

    if as_lower:
        text = text.lower()

    # synonyms replacement
    if synonym:  # if there are synonyms need to replaced
        for key_term in synonym.keys():  # for each key-term that has synonyms
            for term in synonym[key_term]:  # for each synonym of the key-term
                text = text.replace(term, key_term)  # find and replace it

    chain = []
    for e in keyterms:  # for each element in key-terms
        if type(e) is str:  # for signle term
            chain = text2chain(e, keyterms, text, chain)
        elif type(e) is list:  # for a sub-list contained synonyms
            for t in e:
                chain = text2chain(t, keyterms, text, chain)

    chain.sort()  # sort by order of occurrence
    chain = list(x[1] for x in chain)  # keep index of terms only

    prx = np.zeros([len(keyterms), len(keyterms)])  # proximity data format
    for i in range(0, len(chain) - 1):
        prx[chain[i], chain[i + 1]] = 1
        prx[chain[i + 1], chain[i]] = 1
        prx[chain[i], chain[i]] = None  # 对角线的元素赋值为NaN

    # Step 4: calculate PFNet (if necessary)
    if pfnet:
        # similarity --> distances (if necessary)
        if max is not None and min is not None:
            prx = max - prx + min
            # the value that out of range would be set as inf
            prx = np.where((prx > min) & (prx < max), prx, np.inf)

        prx = floyd(prx, r=r)

    # Step 5: convert it to a graph
    start, end = np.where(np.tril(prx) == True)
    pairs = []
    for i in range(0, len(start)):
        pairs.append([keyterms[start[i]], keyterms[end[i]]])
    G.add_edges_from(pairs)

    return G


def text2chain(t, keyterms, text, chain, synonym=False):
    for index in finditer(t, text):  # obtain index of terms in the text
        if chain:
            """

            before add the new index into the list "chain", we need to 
            check the index to avoid the error.

            for example, when obtain a index of term "bees" in the text, it 
            would first check whether this index is contain in the span of 
            term "beeswax", if the answer is "True", this index wouldn't 
            be included in the "chain".

            for this purpose, please insure small terms (e.g., "bees") were 
            after bigger terms (e.g., "beeswax") in the terms list.

            """

            check = False
            for i in chain:
                if index.span()[0] >= i[0][0] and index.span()[1] <= i[0][1] and index.span() != i[0]:
                    check = True
                    break
            if not check:
                if synonym:
                    chain.append([index.span(), keyterms.index(synonym)])
                else:
                    chain.append([index.span(), keyterms.index(t)])
        else:
            if synonym:
                chain.append([index.span(), keyterms.index(synonym)])
            else:
                chain.append([index.span(), keyterms.index(t)])

    return chain

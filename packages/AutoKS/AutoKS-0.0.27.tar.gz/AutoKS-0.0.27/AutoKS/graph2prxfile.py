#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx


def graph2prxfile(
        graph,
        filetype,
        filename,
        keyterm_list=None,
        encoding='UTF-8'
):
    """
    save edges in a graph into a prx file

    :param graph: a NetworkX graph.
    :param filetype: a string specifying the data type to save, can be "pair" or
    "array".
    :param filename: filename of output file.
    :param keyterm_list: a list of key-terms.
    :param encoding: default is "utf-8", which supports most languages, such as
    English, Chinese, Korean, Arabic, etc.
    :return: None.
    """

    try:

        output = None

        if keyterm_list:
            graph.add_nodes_from(keyterm_list)

        if filetype == 'array':
            # convert graph into proximity array
            matrix = (nx.to_numpy_array(
                graph,
                dtype=int,
                nodelist=keyterm_list))  # matrix_str='[[0 1 0]\n [1 0 1]\n...'
            matrix_str = '\n'.join('[{}]'.format(' '.join(str(n) for n in row)) for row in matrix)
            repl = {'[': '',
                    ']': '',
                    ' ': '\t'}
            for i in repl:
                matrix_str = matrix_str.replace(i, repl[i])
                # matrix_str = '0 1 0 1 0\n1 0 1 0 1\n...'

            # print(matrix_str)

            # output content
            if keyterm_list:
                nodes_num = len(keyterm_list)
            else:
                nodes_num = len(graph.nodes)
            output = f"""DATA\nsimilarities\n{nodes_num} item\n1 decimals\n0.1 min\n1 max\nmatrix:\n{matrix_str}"""

        if filetype == 'pair':

            output = ''
            for pair in graph.edges:
                output += f'{pair[0]}\t{pair[1]}\n'

            output = output[:-2]  # remove the last '\n'

        # write file
        if filetype == 'array':
            with open(filename + f'.prx', 'w', encoding=encoding) as f:
                f.write(output)
            print(f'Prx file is saved! File name is "{filename}.prx".')
        elif filetype == 'pair':
            with open(filename + f'.txt', 'w', encoding=encoding) as f:
                f.write(output)
            print(f'Prx file is saved! File name is "{filename}.txt".')

    except IOError:
        print('ERROR!')

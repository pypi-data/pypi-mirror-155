# !/usr/bin/env python
# -*- coding: utf-8 -*-

def read_file(filepath,
              encoding='utf-8'):
    """
    read contents from a .txt file into a list.

    :param filepath: file path of the file.
    :param encoding: default is "utf-8", which supports most languages, such as
    English, Chinese, Korean, Arabic, etc.
    :return: a list contained contents of file.
    """
    content = []
    f = open(filepath, "r", encoding=encoding)
    for line in f.readlines():
        line = line.strip('\n')  # remove "\n" in "node1 \t node2 \n"
        if '\t' in line:
            # split to each element in a list by "\t"
            content.append(line.split('\t'))
        else:
            # split to each element in a list by " " (i.e., space)
            line = line.split(' ')
            if '' in line:
                line.remove('')  # delete the element that have "" value
            content.append(line)
    f.close()
    return content

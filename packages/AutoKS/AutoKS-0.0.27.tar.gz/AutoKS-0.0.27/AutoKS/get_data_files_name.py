#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import walk


def get_data_files_name(init_file_path):

    data = list()

    for cur_dir, sub_dir, included_file in walk(init_file_path):
        if included_file:
            for file in included_file:
                data.append(cur_dir + "/" + file)

    print(f'Get {len(data)} files from {init_file_path}.')

    return data

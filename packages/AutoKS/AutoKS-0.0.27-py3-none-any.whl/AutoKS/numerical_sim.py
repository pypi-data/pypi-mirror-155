#!/usr/bin/env python
# -*- coding: utf-8 -*-

def numerical_sim(value1, value2):
    """
    calculate numerical similarity, see "calc_tversky"

    :param value1: a value.
    :param value2: another value.
    :return: a number of similarity.
    """

    s = 1 - abs(value1 - value2)/max(value1, value2)

    return s

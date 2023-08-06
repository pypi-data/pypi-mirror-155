#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .numerical_sim import *


def calc_surface_matching(
        graph1,
        graph2
):
    """
    calculate surface matching index between graphs.

    see:
    Kopainsky, B., Pirnay-Dummer, P., & Alessi, S. M. (2012). Automated
    assessment of learners' understanding in complex dynamic systems: Automated
    Assessment of Understanding. System Dynamics Review, 28(2), 131-156.

    :param graph1: a NetworkX graph.
    :param graph2: another Networkx graph.
    :return: a number of surface matching.
    """

    links_num1 = graph1.number_of_edges()
    links_num2 = graph2.number_of_edges()
    s = numerical_sim(links_num1, links_num2)

    return s

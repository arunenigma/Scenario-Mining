# -*- coding: utf-8 -*-
from __future__ import division
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"


class DegreeOfMembership(object):
    def __init__(self):
        self.dom_data_list = []

    def findFuzzySet(self, tf_idf_list, span, pivots):
        tf_idf_list_norm = {}
        if not len(tf_idf_list) == 0:
            self.max_tf_idf = max(tf_idf_list.values())
        for word, tf_idf in tf_idf_list.iteritems():
            tf_idf /= self.max_tf_idf
            tf_idf_list_norm[word] = tf_idf

        fuzzy_set_intervals = [pivots[i:i+2] for i in range(len(pivots)-1)]
        for word, tf_idf in tf_idf_list_norm.iteritems():
            fuzzy_sets = []
            for interval in fuzzy_set_intervals:
                if interval[0] <= tf_idf <= interval[1]:
                    for i, s in enumerate(span):
                        if not (i + 1) >= len(span):
                            if (interval[0] in span[i] and interval[1] in span[i]) and (interval[0] in span[i + 1] and interval[1] in span[i + 1]):
                                fuzzy_sets.append([word, tf_idf, i, span[i], i + 1, span[i + 1]])
            self.findDOM(fuzzy_sets)

    def findDOM(self, fuzzy_sets):
        dom_data = []
        dom_1 = self.triangularFunction(fuzzy_sets[0][1], fuzzy_sets[0][3][0], fuzzy_sets[0][3][1], fuzzy_sets[0][3][2])
        dom_data.append([fuzzy_sets[0][0], fuzzy_sets[0][1], fuzzy_sets[0][2], dom_1])
        dom_2 = self.triangularFunction(fuzzy_sets[0][1], fuzzy_sets[0][5][0], fuzzy_sets[0][5][1], fuzzy_sets[0][5][2])
        dom_data[0].extend([fuzzy_sets[0][4], dom_2])
        self.generateDOMTable(dom_data)

    def triangularFunction(self, tf_idf, a, b, c):
        dom = 0.0
        if tf_idf <= a:
            dom += 0
        elif a <= tf_idf <= b:
            dom += (tf_idf - a)/(b - a)
        elif b <= tf_idf <= c:
            dom += (c - tf_idf)/(c - b)
        elif c <= tf_idf:
            dom += 0
        return dom

    def generateDOMTable(self, dom_data):
        self.dom_data_list.append([dom_data[0][0], dom_data[0][1], (dom_data[0][2]), dom_data[0][3], (dom_data[0][4]), dom_data[0][5]])


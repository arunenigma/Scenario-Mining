# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

import numpy as np


class RangeCalculator:
    def __init__(self):
        self.span = []
        self.pivots = []
        self.tf_idf_values = []

    def calculateFilterIRange(self, tf_idf_list):  # tf-idf filter
        tf_idf_list_norm = {}
        if not len(tf_idf_list) == 0:
            self.max_tf_idf = max(tf_idf_list.values())
        for word, tf_idf in tf_idf_list.iteritems():
            tf_idf /= self.max_tf_idf
            tf_idf_list_norm[word] = tf_idf
        self.tf_idf_values = tf_idf_list_norm.values()
        avg_tf_idf = np.mean(self.tf_idf_values, dtype=np.float128)
        below_avg_values = []
        above_avg_values = []

        for value in self.tf_idf_values:
            if value <= avg_tf_idf:
                below_avg_values.append(value)
            if value >= avg_tf_idf:
                above_avg_values.append(value)

        below_avg_values_pivot = np.mean(below_avg_values, dtype=np.float128)
        above_avg_values_pivot = np.mean(above_avg_values, dtype=np.float128)
        lowest_values = []
        highest_values = []

        for value in below_avg_values:
            if value <= below_avg_values_pivot:
                lowest_values.append(value)
        for value in above_avg_values:
            if value >= above_avg_values_pivot:
                highest_values.append(value)

        lowest_values_pivot = np.mean(lowest_values, dtype=np.float128)
        highest_values_pivot = np.mean(highest_values, dtype=np.float128)

        very_low = []
        very_high = []

        for value in lowest_values:
            if value <= lowest_values_pivot:
                very_low.append(value)
        for value in highest_values:
            if value >= highest_values_pivot:
                very_high.append(value)

        very_low_pivot = np.mean(very_low, dtype=np.float128)
        very_high_pivot = np.mean(very_high, dtype=np.float128)

        extremely_low = []
        extremely_high = []

        for value in very_low:
            if value <= very_low_pivot:
                extremely_low.append(value)

        for value in very_high:
            if value >= very_high_pivot:
                extremely_high.append(value)

        extremely_low_pivot = np.mean(extremely_low, dtype=np.float128)
        extremely_high_pivot = np.mean(extremely_high, dtype=np.float128)

        # adding overlap span (cox 1999)
        # triangle & triangle -> 25% overlap
        self.pivots.extend(
            [0, extremely_low_pivot, very_low_pivot, lowest_values_pivot, below_avg_values_pivot, avg_tf_idf,
             above_avg_values_pivot, highest_values_pivot, very_high_pivot, extremely_high_pivot, 1])
        #print self.pivots
        self.span.append([0, 0, extremely_low_pivot])
        self.span.append([0, extremely_low_pivot, very_low_pivot])
        self.span.append([extremely_low_pivot, very_low_pivot, lowest_values_pivot])
        self.span.append([very_low_pivot, lowest_values_pivot, below_avg_values_pivot])
        self.span.append([lowest_values_pivot, below_avg_values_pivot, avg_tf_idf])
        self.span.append([below_avg_values_pivot, avg_tf_idf, above_avg_values_pivot])
        self.span.append([avg_tf_idf, above_avg_values_pivot, highest_values_pivot])
        self.span.append([above_avg_values_pivot, highest_values_pivot, very_high_pivot])
        self.span.append([highest_values_pivot, very_high_pivot, extremely_high_pivot])
        self.span.append([very_high_pivot, extremely_high_pivot, 1])
        self.span.append([extremely_high_pivot, 1, 1])

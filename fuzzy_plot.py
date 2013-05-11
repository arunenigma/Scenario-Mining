# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

import numpy as np
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random


class FuzzyPlotFilterI(object):
    def drawFuzzyPlotFilterI(self, tf_idf_values, span):
        fig = Figure(figsize=(9, 7))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        ax.set_title("Fuzzy Plot", fontsize=14)
        ax.set_xlabel("Tf-Idf (Normalized)", fontsize=12)
        ax.set_ylabel("Degree of Membership", fontsize=12)
        patches = []

        for i in range(len(span)):
            polygon = Polygon([[span[i][0],0],[span[i][1],1],[span[i][2],0]], True)
            patches.append(polygon)

        colors = range(len(span))
        p = PatchCollection(patches, cmap=matplotlib.cm.jet, alpha=.4)
        p.set_array(np.array(colors))
        ax.add_collection(p)
        ax.axis([0, 1, 0, 1])
        r = random.random()
        canvas.print_figure(str(r)+'fuzzy_plot.pdf', dpi=700)

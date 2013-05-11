# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random

class ScatterPlot(object):
    def drawScatterPlot(self, tf_idf_values):
        x_limit = max(tf_idf_values)
        fig = Figure(figsize=(9, 7))
        canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        population = {}

        for value in set(tf_idf_values):
            population[value] = tf_idf_values.count(value)
        ax.grid(True, linestyle='-', color='0.75')
        ax.scatter(population.keys()[:-1], population.keys()[1:], c=population.keys()[:-1], s=population.values(),
            alpha=0.75)
        ax.set_title("Scatter Plot for Word Clusters", fontsize=14)
        ax.set_xlabel("Tf-Idf (Normalized)", fontsize=12)
        ax.set_ylabel("Tf-Idf (Normalized)", fontsize=12)
        ax.axis([0, x_limit, 0, x_limit])
        r = random.random()
        canvas.print_figure(str(r)+'scatter_plot.png', dpi=700)

# -*- coding: utf-8 -*-
from __future__ import division
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from ordereddict import OrderedDict
from math import ceil
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from operator import itemgetter

def kmeans(data, k):
    """
    * This def takes a array of integers and the number of clusters to create.:
    * It returns a multidimensional array containing the original data organized
    * in clusters.
    *
    * @param array data
    * @param int k
    *
    * @return array
    """
    cPositions = assign_initial_positions(data, k)
    clusters = OrderedDict()
    while True:
        changes = kmeans_clustering(data, cPositions, clusters)
        if not changes:
            return kmeans_get_cluster_values(data, clusters)
        cPositions = kmeans_recalculate_cpositions(data, cPositions, clusters)


def kmeans_clustering(data, cPositions, clusters):
    """
    """
    nChanges = 0
    for dataKey, value in enumerate(data):#.items():
        minDistance = None
        cluster = None
        for k, position in cPositions.items():
            dist = distance(value, position)
            if None is minDistance or minDistance > dist:
                minDistance = dist
                cluster = k
        if not clusters.has_key(dataKey) or clusters[dataKey] != cluster:
            nChanges += 1
        clusters[dataKey] = cluster
    return nChanges


def kmeans_recalculate_cpositions(data, cPositions, clusters):
    kValues = kmeans_get_cluster_values(data, clusters)
    for k, position in cPositions.items():
        if not kValues.has_key(k):
            cPositions[k] = 0
        else:
            cPositions[k] = kmeans_avg(kValues[k])
            #cPositions[k] = empty(kValues[k]) ? 0 : kmeans_avg(kValues[k])
    return cPositions


def kmeans_get_cluster_values(data, clusters):
    values = OrderedDict()
    for dataKey, cluster in clusters.items():
        if not values.has_key(cluster):
            values[cluster] = []
        values[cluster].append(data[dataKey])
    return values


def kmeans_avg(values):
    n = len(values)
    total = sum(values)
    if n == 0:
        return 0
    else:
        return total / (n * 1.0)


def distance(v1, v2):
    """
    * Calculates the distance (or similarity) between two values. The closer
    * the return value is to ZERO, the more similar the two values are.
    *
    * @param int v1
    * @param int v2
    *
    * @return int
    """
    return abs(v1 - v2)


def assign_initial_positions(data, k):
    """
    * Creates the initial positions for the given
    * number of clusters and data.
    * @param array data
    * @param int k
    *
    * @return array
    """
    small = min(data)
    big = max(data)
    num = ceil((abs(big - small) * 1.0) / k)
    cPositions = OrderedDict()
    while k > 0:
        k -= 1
        cPositions[k] = small + num * k
    return cPositions

def readData(f, tf_idf_list):
    f = f.readlines()
    for item in f:
        item = item.split()
        tf_idf = item[1]
        tf_idf_list.append(tf_idf)
    return tf_idf_list


def printClusterData(f, la, range_estimator):

    col = ['r', 'y', 'm', 'c', 'b', 'g', 'r', 'y', 'm', 'c']
    ax.hold(True)
    l = len(f)
    x = range(l)
    ax.set_ylim(-50, 350)
    ax.set_xlim(-.1, 1.1)

    #plt.xticks([.01,.02,.03,.04,.05,.1,.15,.2,.25,.3,.4,.5,1])

    '''
    fig = Figure(figsize=(9, 7))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    population = {}

    for value in set(f):
        population[value] = f.count(value)
    ax.grid(True, linestyle='-', color='0.75')
    ax.scatter(f,x, c=population.keys(), s=population.values(),marker='o', alpha=0.75)
    ax.set_title("Scatter Plot for Word Clusters", fontsize=14)
    ax.set_xlabel("Tf-Idf (Normalized)", fontsize=12)
    ax.set_ylabel("Tf-Idf (Normalized)", fontsize=12)


    canvas.print_figure('cluster_plot.png', dpi=700)

    '''

    #plt.grid(True, linestyle='-', color='0.75')
    ax.scatter(f, x, s=30, c=col[i], marker='o', alpha=0.75)
    piv = 0
    cen = sum(f)/l
    range_estimator.append([min(f), cen, max(f)])
    print
    for dd, ele in enumerate(f):
        if (dd+1) < len(f) and ele < cen < f[dd+1]:
            piv = dd
    print piv
    # centroids
    ax.scatter(cen,piv, marker='o', s = 300, linewidths=1, c='w', alpha=0.60)
    ax.scatter(cen,piv, marker='x', s = 300, linewidths=1, c='k', alpha=0.60 )
    #plt.axvline(x=cen, ymin = piv, ymax=piv, linewidth=0.3, color='black')
    ax.vlines(x=cen, ymin=-50, ymax=piv, color='k', linestyles='solid')

    #plt.show()
    fig = "cluster.png"
    #plt.savefig(fig)
    canvas.print_figure('cluster_plot.pdf', dpi=700)


if __name__ == '__main__':


    tf_idf_list = []
    f = open('out.txt','r')
    x = readData(f, tf_idf_list)
    x = [float(e) for e in x ]
    la = len(x)
    y = kmeans(x, 10)
    fig = Figure(figsize=(9, 7))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    range_estimator = []

    for i, f in y.iteritems():
        print i, f
        printClusterData(f, la, range_estimator)
    #print range_estimator
    ranges = sorted(range_estimator, key=itemgetter(1))
    for range in ranges:
        print range[0], range[1], range[2]



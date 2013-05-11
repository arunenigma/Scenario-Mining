from __future__ import division
from fuzzycmeans import *
from random import uniform
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from ordereddict import OrderedDict


def printClusters(tf_idf_values, dom_values, ind, centroids):
    xy_dict = dict(zip(tf_idf_values, dom_values))
    xy_dict_ordered = OrderedDict(sorted(xy_dict.items(), key=lambda item: item[0]))
    colors = ['r', 'y', 'm', 'c', 'b', 'g', 'r', 'y', 'm', 'c']
    ax.hold(True)
    ax.set_ylim(0, 1.1)
    ax.set_xlim(0, 1)
    #plt.grid(True, linestyle='-', color='0.75')
    ax.scatter(xy_dict_ordered.keys(), xy_dict_ordered.values(), s=30, c=colors[ind], marker='o', alpha=0.75, linewidths=.1)
    ax.plot(xy_dict_ordered.keys(), xy_dict_ordered.values(), linestyle='-', c=colors[ind], alpha=.40)
    # centroids
    ax.scatter(centroids[ind], 1, marker='o', s=300, linewidths=1, c='w', alpha=0.60)
    ax.scatter(centroids[ind], 1, marker='x', s=300, linewidths=1, c='k', alpha=0.60 )
    ax.vlines(x=centroids[ind], ymin=0, ymax=1, color='k', linestyles='solid', alpha=0.40)

    #avg_dom = sum(dom_values)/len(dom_values)
    #min_val = min([tf_idf for index, tf_idf in enumerate(tf_idf_values) if dom_values[index] > .5])
    #max_val = max([tf_idf for index, tf_idf in enumerate(tf_idf_values) if dom_values[index] > .5])
    #ax.plot([min_val, centroids[ind], max_val], [0, 1, 0], linewidth=0.3, color='black')
    #print min_val, max_val
    canvas.print_figure('arun_plot.pdf', dpi=700)

if __name__ == '__main__':
    #inputs = [uniform(0,1) for i in range(25)]
    tf_idf_list = []
    f = open('out.txt', 'r').readlines()
    for item in f:
        item = item.split()
        tf_idf = item[1]
        tf_idf_list.append(tf_idf)
    # demo 10 clusters
    inputs = [float(tf_idf) for tf_idf in tf_idf_list]

    c = 10  # number of clusters
    m = 2.0
    mfs = [[uniform(0, 1) for i in range(c)] for i in range(len(inputs))]  # membership functions
    fcm = FuzzyCMeans(inputs, mfs, m)

    print "After 20 iterations, the algorithm converged to the centers:"
    print fcm(emax=0)
    centroids = fcm(emax=0)
    #print
    #print "The membership values for the examples are given below:"
    memberships = fcm.mfs
    #print memberships
    _, C = memberships.shape
    fig = Figure(figsize=(9, 7))
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)

    for column in range(C):
        #print column
        tf_idf_values = []
        dom_values = []
        cluster = memberships[:, column]
        cluster = [membership / max(cluster) for membership in cluster]
        for m, membership in enumerate(cluster):
            tf_idf_values.append(inputs[m])
            dom_values.append(membership)
        printClusters(tf_idf_values, dom_values, column, centroids)

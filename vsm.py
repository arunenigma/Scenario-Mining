#!/usr/bin/env/python
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.pylab import plt
from matplotlib import cm
import numpy as np
import csv
import sys


class VectorSpaceModel(object):
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
        self.doc_A = {}
        self.doc_B = {}
        self.doc_vec_A = []
        self.doc_vec_B = []

    def readCsvFiles(self):
        self.f1.next()
        self.f2.next()
        for row in self.f1:
            self.doc_A[row[0]] = float(row[1])
        for row in self.f2:
            self.doc_B[row[0]] = float(row[1])
        for word, pi_score_A in self.doc_A.iteritems():
            try:
                pi_score_B = self.doc_B[word]
                self.doc_vec_A.append(float(pi_score_A))
                self.doc_vec_B.append(float(pi_score_B))

            except KeyError:
                self.doc_vec_A.append(float(pi_score_A))
                self.doc_vec_B.append(0.0)

    def cosSimilarity(self):
        num = np.dot(self.doc_vec_A, self.doc_vec_B)
        denum = (np.sqrt(np.dot(self.doc_vec_A, self.doc_vec_A)) * np.sqrt(np.dot(self.doc_vec_B, self.doc_vec_B)))
        cos_sim = num / denum
        print cos_sim

    def drawSurfacePlot(self, f1):
        """
            Method to draw a surface plot for test spec
            using Word Rank | Tf-Idf Score | PI

        """
        test_doc = {}
        f1.next()
        for row in f1:
            test_doc[row[0]] = [row[1], row[2]]
        sorted_test_doc = sorted(test_doc.items(), key=lambda e: e[1][0], reverse=True)

        word_rank = []
        PI_list = []
        tf_idf_list = []

        for i, word in enumerate(sorted_test_doc):
            word_rank.append(i + 1)
            PI_list.append(word[1][0])
            tf_idf_list.append(word[1][1])

        PI_list = [float(pi) for pi in PI_list]
        tf_idf_list = [float(tf_idf) for tf_idf in tf_idf_list]
        fig = plt.figure()
        ax = Axes3D(fig)
        X = word_rank
        X_clone = word_rank
        Y = tf_idf_list
        X, Y = np.meshgrid(X, Y)
        print X
        # Z should be a function of X and Y
        Z = PI_list
        X_clone, Z = np.meshgrid(X_clone, Z)
        ax.plot_surface(X, Y, Z, rstride=10, cstride=10, cmap=plt.cm.RdBu, alpha=None)
        #ax.contour(X, Y, Z, zdir='x', offset=-4, cmap=cm.hsv)
        #ax.contour(Y, Y, Z, zdir='y', offset=4, cmap=cm.hsv)
        #ax.contour(Y, Y, Z, zdir='z', offset=-2, cmap=cm.hsv)
        #ax.set_zlim(0, 1)
        plt.show()

if __name__ == '__main__':
    f1 = csv.reader(open(sys.argv[1], 'rb'))
    f2 = csv.reader(open(sys.argv[2], 'rb'))
    v = VectorSpaceModel(f1, f2)
    v.readCsvFiles()
    v.cosSimilarity()
    #v.drawSurfacePlot(f1)



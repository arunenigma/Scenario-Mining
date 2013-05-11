import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pylab as plt
from matplotlib import cm

class SurfacePlotCOG(object):
    def drawSurfacePlot(self, cog_list):
        fig = plt.figure()
        ax = Axes3D(fig)
        X = [] # some list
        Y = [] # some list
        X, Y = np.meshgrid(X, Y)
        # Z should be a function of X and Y
        Z = []

        # cmap colors
        # cmap = {'gray':cm.gray,'pink':cm.pink,'hot':cm.hot,'jet':cm.jet,'summer':cm.summer,'spring':cm.spring,\'winter':cm.winter,'autumn':cm.autumn,'flag':cm.flag,'hsv':cm.hsv,'prism':cm.prism,\'stern':cm.gist_stern,'rainbow':cm.gist_rainbow,'earth':cm.gist_earth,'ncar':cm.gist_ncar,'cool':cm.cool,\'copper':cm.copper,'bone':cm.bone,'rdbu':cm.RdBu}

        ax.plot_surface(Y, Y, Z, rstride=1, cstride=1, cmap=plt.cm.hsv, alpha=None)
        ax.contour(Y, Y, Z, zdir='x', offset=-4, cmap=cm.hsv)
        ax.contour(Y, Y, Z, zdir='y', offset=4, cmap=cm.hsv)
        ax.contour(Y, Y, Z, zdir='z', offset=-2, cmap=cm.hsv)
        ax.set_zlim(0, 1)
        plt.show()

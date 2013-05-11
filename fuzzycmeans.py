# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

from numpy import dot, array, sum, zeros, outer
from numpy.numarray import reshape

################################################################################
# Fuzzy C-Means class
################################################################################


class FuzzyCMeans(object):
    def __init__(self, inputs, mfs, m):
        """
         m
           Aggregation value. The bigger it is, the smoother will
           be the clustering. 'm' must be bigger than 1. Its default value is set to 2
        """
        # double underscore in front denotes the variable cannot be over ridden by any sub classes
        self.__inputs = array([inputs]).transpose()
        self.__mfs = array(mfs)
        self.m = m
        # self.__c (double underscore in front of the method denotes that the method cannot be
        # over ridden by sub classes)
        self.__c = self.centers()

    def __get_c(self):
        return self.__c

    def __set_c(self, c):
        self.__c = array(reshape(c, self.__c.shape))
    c = property(__get_c, __set_c)

    def __get_mfs(self):
        return self.__mfs
    mfs = property(__get_mfs, None)

    def __get_inputs(self):
        return self.__inputs
    inputs = property(__get_inputs, None)

    def centers(self):
        mf_aggregated = self.__mfs * self.m
        c = dot(self.__inputs.transpose(), mf_aggregated)/sum(mf_aggregated, axis=0)
        self.__c = c.transpose()
        return self.__c

    def membership(self):
        inputs = self.__inputs
        c = self.__c
        M, _ = inputs.shape
        C, _ = c.shape
        r = zeros((M, C))
        m1 = 1. / (self.m - 1.)
        for k in range(M):
            den = sum((inputs[k] - c) ** 2., axis=1)
            frac = outer(den, 1./den) ** m1
            r[k, :] = 1./sum(frac, axis=1)
        self.__mfs = r
        return self.__mfs

    def step(self):
        old = self.__mfs
        self.membership()
        self.centers()
        return sum(self.__mfs - old) ** 2.

    def __call__(self, emax=1.e-10, imax=20):
        error = 1.
        i = 0
        while error > emax and i < imax:
            error = self.step()
            i += 1
        return self.c

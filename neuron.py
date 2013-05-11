"""
from __future__ import division
__author__ = 'arunprasathshankar'
import itertools
import operator
class NeuroFuzzySystem(object):

    def __init__(self):
        self.word_list = []
        self.cog_list = []

    def neuroFuzzyModelling(self, tf_idf_list, f1, f2, f3):
        for word, tf_idf in tf_idf_list.iteritems():
            for x in f1:
                if word == x[0]:
                    for y in f2:
                        if word == y[0]:
                            for z in f3:
                                if word == z[0]:
                                    A = x[2]*x[3]
                                    B = x[4]*x[5]
                                    C = y[2]*y[3]+1
                                    D = y[4]*y[5]+1
                                    E = z[2]*z[3]+1
                                    F = z[4]*z[5]+1
                                    mfs = [[A,B],[C,D],[E,F]]
                                    weights = sum([x[3],x[5],y[3],y[5],z[3],z[5]])
                                    rule_inputs = list(itertools.product(*mfs))
                                    len_comb = len(rule_inputs)
                                    weight_factor = (len(mfs)*len_comb)/6 # 6 --> write code to find this automatically
                                    weights *= weight_factor
                                    rule_inputs = sum([sum(r) for r in rule_inputs])
                                    self.defuzzify(word, tf_idf, rule_inputs, weights )

    def defuzzify(self, word, tf_idf, rule_inputs, weights):
        cog = rule_inputs / weights
        #print word, tf_idf, cog
        self.word_list.append(word)
        self.cog_list.append(cog)


    def normCOG(self):
        max_cog = max(self.cog_list)
        self.cog_list = [cog/max_cog for cog in self.cog_list]
        word_rank = dict(zip(self.word_list, self.cog_list))
        sorted_word_rank = sorted(word_rank.iteritems(), key=operator.itemgetter(1))
        for item in sorted_word_rank:
            print item[0], item[1]
__author__ = 'arunprasathshankar'


"""

from __future__ import division
# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

# Neural Networks Without Back Propagation
from sympy import Matrix, zeros, ones, pprint
from matplotlib.pylab import plt
import random
import math

def randomWeightMatrix(x,y):
    mat = ones([x,y])
    f = lambda x: random.uniform(0,1) * x
    mat = mat.applyfunc(f)
    return mat

def sigmoid(x):
    # sigmoid function
    return math.tanh(x)

def dsigmoid(y):
    return 1 - y ** 2

class NeuralNetwork(object):
    def __init__(self, tf_idf_list, c1, c2, c3):
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3


        # number of nodes in input, hidden and output layers
        self.input_nodes =  + 1 # +1 for bias
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # initializing node activations
        self.activation_input = Matrix([1.0] * self.input_nodes)
        self.activation_hidden = Matrix([1.0] * self.hidden_nodes)
        self.activation_output = Matrix([1.0] * self.output_nodes)

        # create node weight matrices
        self.weights_input_hidden = randomWeightMatrix(self.input_nodes, self.hidden_nodes)
        self.weights_hidden_output = randomWeightMatrix(self.hidden_nodes, self.output_nodes)

        # create last change in weights matrices for momentum
        self.weights_input_hidden_last_change = zeros([self.input_nodes, self.hidden_nodes])
        self.weights_hidden_output_last_change =  zeros([self.hidden_nodes, self.output_nodes])

    def runNN(self, inputs):
        # activating all neurons inside NN
        if len(inputs) != self.input_nodes - 1:
            raise ValueError('Wrong number of inputs, should have %i inputs.' % (self.input_nodes-1))

        for i in range(self.input_nodes - 1):
            self.activation_input[i] = inputs[i]

        for j in range(self.hidden_nodes):
            sum = 0.0
            for i in range(self.input_nodes):
                sum += (self.activation_input[i] * self.weights_input_hidden[i,j])
            self.activation_hidden[j] = sigmoid(sum)

        for k in range(self.output_nodes):
            sum = 0.0
            for j in range(self.hidden_nodes):
                sum += (self.activation_hidden[j] * self.weights_hidden_output[j,k]) # {2} <--
            self.activation_output[k] = sigmoid(sum)

        return self.activation_output

    def testNN(self, training_set):
        for r in range(training_set.rows):
            inputs = training_set[r, :][0]
            targets = training_set[r, :][1]
            print 'Inputs:', inputs, '\tOutput', NeuralNetwork.runNN(self, inputs), '\tTarget', targets

    def trainNN(self, training_set, max_iterations = 1000, learning_rate=0.5, momentum=0.1):
        error_list = []
        for i in range(max_iterations):
            error = 0.0
            for r in range(training_set.rows):
                inputs = training_set[r,:][0]
                targets = training_set[r,:][1]
                self.runNN(inputs)
        self.testNN(training_set) # test_set ==> training set here

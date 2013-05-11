from __future__ import division
# -*- coding: utf-8 -*-
__author__ = "Arunprasath Shankar"
__copyright__ = "Copyright 2012, Arunprasath Shankar"
__license__ = "GPL"
__version__ = "1.0.1"
__email__ = "axs918@case.edu"

# Neural Networks Back Propagation
from sympy import Matrix, zeros, ones, pprint
from matplotlib.pylab import plt
import random
import math


def randomWeightMatrix(x, y):
    mat = ones([x, y])
    f = lambda x: random.uniform(0, 1) * x
    mat = mat.applyfunc(f)
    return mat


def sigmoid(x):
    # sigmoid function
    return math.tanh(x)


def dsigmoid(y):
    return 1 - y ** 2


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes):
        # number of nodes in input, hidden and output layers
        self.input_nodes = input_nodes + 1 # +1 for bias
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

    def backPropagateNN(self, targets, learning_rate, momentum):
        # finding instantaneous rate of change of Error w.r.t weight from node j(hidden) to node k(output).
        # output_deltas are defined as an attribute of each output node. It is not the final rate we need.
        # To get the final rate we must multiply the delta by the activation of the hidden layer node in question.
        # This multiplication is done according to chain rule as we are taking the derivative of the activation function of the output node.
        # dE/dw[j][k] = (t[k] - ao[k]) * s'(SUM(w[j][k]*ah[j]))
        # output_deltas[k] =  error * dsigmoid(self.activation_output[k]) <-- equivalent code below {1}
        # SUM(w[j][k]*ah[j]) --> sum += (self.activation_hidden[j] * self.weights_hidden_output[k]) <-- equivalent code above {2}

        if len(targets) != self.output_nodes:
            raise ValueError('Wrong number of target values, should have %i targets.' % self.output_nodes)

        #calculate output deltas
        output_deltas = Matrix([0.0] * self.output_nodes)
        for k in range(self.output_nodes):
            error = targets[k] - self.activation_output[k]
            output_deltas[k] =  error * dsigmoid(self.activation_output[k]) # {1} <--

        #update hidden_output weights
        for j in range(self.hidden_nodes):
            for k in range(self.output_nodes):
            # output_deltas[k] * self.ah[j] is the full derivative of dE/dw[j][k]
                change = output_deltas[k] * self.activation_hidden[j]
                self.weights_hidden_output[j, k] += learning_rate * change + momentum * \
                                                    self.weights_hidden_output_last_change[j, k]
                self.weights_hidden_output_last_change[j, k] = change

        # calculate hidden deltas
        hidden_deltas = Matrix([0.0] * self.hidden_nodes)
        for j in range(self.hidden_nodes):
            error = 0.0
            for k in range(self.output_nodes):
                error += output_deltas[k] * self.weights_hidden_output[j, k]
            hidden_deltas[j] = error * dsigmoid(self.activation_hidden[j])

        #update input_hidden weights
        for i in range(self.input_nodes):
            for j in range(self.hidden_nodes):
                change = hidden_deltas[j] * self.activation_input[i]
                self.weights_input_hidden[i, j] += learning_rate * change + momentum * \
                                                   self.weights_input_hidden_last_change[i, j]
                self.weights_input_hidden_last_change[i, j] = change

        # 1/2 for differential convenience & **2 for modulus
        error = 0.0
        for k in range(len(targets)):
            error += 0.5 * (targets[k] - self.activation_output[k]) ** 2
        return error

    def testNN(self, training_set):
        for r in range(training_set.rows):
            inputs = training_set[r, :][0]
            targets = training_set[r, :][1]
            print 'Inputs:', inputs, '\tOutput', NeuralNetwork.runNN(self, inputs), '\tTarget', targets

    def trainNN(self, training_set, max_iterations=1000, learning_rate=0.5, momentum=0.1):
        error_list = []
        for i in range(max_iterations):
            error = 0.0
            for r in range(training_set.rows):
                inputs = training_set[r, :][0]
                targets = training_set[r, :][1]
                self.runNN(inputs)
                error += self.backPropagateNN(targets, learning_rate, momentum)
            if i % 100 == 0:
                print 'Combined Error = ', error
                error_list.append(error)

        self.testNN(training_set)  # test_set ==> training set here
        self.drawErrorPlot(error_list)

    def drawErrorPlot(self, error_list):
        plt.xlim(0, len(error_list))
        plt.xlabel('Squared Error')
        plt.plot(error_list)
        plt.show()

if __name__ == '__main__':
    nn = NeuralNetwork(2, 2, 1)
    training_set = Matrix([
        [[0, 0], [1]],
        [[0, 1], [1]],
        [[1, 0], [1]],
        [[1, 1], [0]]
    ])
    nn.trainNN(training_set)


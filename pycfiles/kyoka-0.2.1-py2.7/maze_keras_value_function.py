# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sample/maze/maze_keras_value_function.py
# Compiled at: 2016-10-08 03:49:35
import math
from sample.maze.maze_domain import MazeDomain
from kyoka.value_function.base_keras_action_value_function import BaseKerasActionValueFunction
from keras.models import Sequential
from keras.layers.core import Dense, Activation
import numpy as np

class MazeKerasValueFunction(BaseKerasActionValueFunction):

    def __init__(self, domain):
        BaseKerasActionValueFunction.__init__(self)
        self.domain = domain
        self.maze_shape = domain.get_maze_shape()

    def generate_model(self):
        input_dim = self.maze_shape[0] * self.maze_shape[1]
        model = Sequential()
        model.add(Dense(100, input_shape=(input_dim,)))
        model.add(Activation('relu'))
        model.add(Dense(1))
        model.compile(loss='mse', optimizer='adam')
        return model

    def transform_state_action_into_input(self, state, action):
        flatten = lambda l: [ item for sublist in l for item in sublist ]
        next_state = self.domain.transit_state(state, action)
        onehot = [ [ 1 if next_state == (row, col) else 0 for col in range(self.maze_shape[1]) ] for row in range(self.maze_shape[0])
                 ]
        return flatten(onehot)

    def fetch_training_metric(self, metrics):
        return metrics

    def predict_value(self, model, X):
        return model.predict(np.array([X]))[0][0]
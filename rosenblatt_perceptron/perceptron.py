#!/usr/bin/env python
#
# Perceptron module
#
# by Bruno Daniel Lima


"""Perceptron module"""


# Installed packages
import numpy as np


class Perceptron:
    """Perceptron"""

    def __init__(self,
                 bias: int,
                 learning_rate:float,
                 height:int,
                 width:int) -> None:
        self.bias = bias
        self.learning_rate = learning_rate
        self.weights = np.zeros((height, width))

    def fit(self, should_activate:bool, figure) -> None:
        """Fit weights"""
        ## TODO: solve weight calculation

        is_activated, _ = self.predict(figure)

        if should_activate == is_activated:
            return

        sign = 1 if should_activate else -1

        self.weights += sign * self.learning_rate * figure

    def predict(self, figure) -> bool:
        """
        Depending of the weights, the neuron
        will be activated or not
        """

        # Multiply each array by its weight
        weighted_array = np.dot(figure, self.weights)

        # Sum all array items
        sum_result = np.sum(weighted_array)

        is_activated = sum_result > self.bias

        return is_activated, sum_result

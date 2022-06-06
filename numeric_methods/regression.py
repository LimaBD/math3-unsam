#!/usr/bin/env python3
#
# Regression module
#
# by Bruno Daniel Lima


"""Regresion module"""


# Installed packages
import matplotlib.pyplot as plt


class Point:
    """A sinple point"""

    def __init__(self, coor_x: float, coor_y: float):
        self.coor_x = coor_x
        self.coor_y = coor_y


class LinearRegression:
    """
    This is used to obtain values of
    a line through linear regression
    """

    def __init__(self, points: list):
        self.points = points

        # Global states
        #
        # Increases memory used but reduces number of operations
        # (execution time still be high because this is Python)
        #
        # Note that we cant change the points one this is initialized
        self.sum_x = self.sum_y = 0
        for point in self.points:
            self.sum_x += point.coor_x
            self.sum_y += point.coor_y
        self.points_count = len(self.points)
        self.slope = self.calc_slope()
        self.y_interception = self.calc_y_interception()

    def calc_slope(self) -> float:
        """
        Calculate slope of best line
        using ordinary least squares
        """
        # result = (nΣxi*yi – Σxi*Σyi) / (nΣxi^2 – (Σxi)^2)

        sum_xy = 0
        sum_x_2 = 0
        for point in self.points:
            sum_xy += point.coor_x * point.coor_y # Σxi*yi
            sum_x_2 += point.coor_x ** 2 # Σxi^2

        # nΣxi*yi – Σxi*Σyi
        dividend = self.points_count * sum_xy
        dividend -= self.sum_x * self.sum_y

        # nΣxi^2 – (Σxi)^2
        divisor = self.points_count * sum_x_2
        divisor -= self.sum_x**2

        return dividend / divisor

    def get_slope(self):
        """
        Returns slope of best line
        using ordinary least squares
        """
        return self.slope

    def calc_y_interception(self) -> float:
        """
        Calculate y interception of best line
        using ordinary least squares
        """
        # result = (Σyi – aΣxi) / n

        dividend = self.sum_y
        dividend -= self.get_slope() * self.sum_x

        return dividend / self.points_count

    def get_y_interception(self):
        """
        Returns y interception of best line
        using ordinary least squares
        """
        return self.y_interception

    def get_function(self) -> str:
        """
        Returns best line using
        ordinary least squares
        """
        return f'{self.slope}x+{self.y_interception}'

    def get_square_error(self) -> float:
        """
        Returns square error of best line
        using ordinary least squares
        """
        # error = Σ(axi + b – yi)2

        result = 0.0
        for point in self.points:
            temp = self.slope * point.coor_x
            temp += self.y_interception
            temp -= point.coor_y
            result += temp ** 2

        return result

    def calc(self, x_value:int) -> float:
        """
        Get result of f(x) using the line obtained
        using ordinary least squares
        """
        return self.slope * x_value + self.y_interception

    def get_domain(self):
        """Returns min and max X values"""
        min_x = max_x = self.points[0].coor_x
        for point in self.points:
            min_x = min(min_x, point.coor_x)
            max_x = max(max_x, point.coor_x)
        return [min_x, max_x]

    def graph(self):
        """
        Print graph of points and best line
        using ordinary least squares
        """

        # Set coordinates to draw line
        linear_x = [self.get_domain()[0], self.get_domain()[-1]]
        linear_y = []
        for value in linear_x:
            linear_y.append(self.calc(value))

        # Set coordinates to draw  points
        for point in self.points:
            plt.scatter(point.coor_x, point.coor_y)

        plt.plot(linear_x, linear_y, '-r', label=self.get_function())
        plt.grid()
        plt.show()

#!/usr/bin/env python
#
# Random Figure generator module
#
# by Bruno Daniel Lima


"""Random figure generator module"""


# Installed packages
import numpy as np


# Standard packages
import random


class FigureGenerator:
    """
    Random figure generator abstract class
    """

    def __init__(self) -> None:

        # Canvas dimensions
        self.canvas_height = 100
        self.canvas_width = 100

        # Figure min dimensions
        #
        # This calculation avoids
        # problems if canvas dim changes
        self.min_height = int(self.canvas_height / 4)
        self.min_width = int(self.canvas_width / 4)

        # Figure max dimensions
        #
        # This calculation avoids problems
        # if figure min dim changes
        self.max_height = self.canvas_height * 1.5
        self.max_width = self.min_width * 1.5

    def set_canvas_dimensions(self,
                              height:int,
                              width:int) -> None:
        """Set canvas (array) dimensions"""
        self.canvas_height = height
        self.canvas_width = width

    def set_min_figure(self,
                       height:int,
                       width:int) -> None:
        """Set minimum figure dimensions"""
        self.min_height = height
        self.min_width = width

    def set_max_figure(self,
                       height:int,
                       width:int) -> None:
        """Set maximun figure dimensions"""
        self.max_height = height
        self.max_width = width

    def generate(self) -> list:
        """Generate random figure"""
        # NOTE: this method must be
        #       overriden by child.
        return []


class RectangleGenerator(FigureGenerator):
    """
    Random rectangle generator class
    """

    def generate(self) -> list:
        """Generate random figure"""
        canvas = np.zeros((self.canvas_height, self.canvas_width))

        # X axis
        while True:
            first_x = random.randint(1, self.canvas_width - 1)
            second_x = random.randint(1, self.canvas_width - 1)
            if self.max_width > abs(first_x - second_x) > self.min_width:
                break

        # Y axis
        while True:
            first_y = random.randint(1, self.canvas_height - 1)
            second_y = random.randint(1, self.canvas_height - 1)
            if self.max_height > abs(first_y - second_y) > self.min_height:
                break

        canvas[min(first_y, second_y):max(first_y, second_y),
               min(first_x, second_x):max(first_x, second_x)] = 1

        return canvas


class CircleGenerator(FigureGenerator):
    """
    Random circle generator class
    """

    def generate(self) -> list:
        """Generate random figure"""
        canvas = np.zeros((self.canvas_height, self.canvas_width))

        max_radius = min(self.max_height, self.max_width)
        min_radius = min(self.min_height, self.min_width)

        # specify circle parameters: centre ij and radius
        while True:
            center_x = random.randint(1, self.canvas_width - 1)
            center_y = random.randint(1, self.canvas_height - 1)
            radius = random.randint(1, max_radius - 1)

            # Check radius
            if not min_radius < radius * 2 < max_radius:
                continue

            # Check x dimensions
            if not 0 < center_x + radius < self.canvas_width:
                continue
            if not 0 < center_x - radius < self.canvas_width:
                continue

            # Check y dimensions
            if not 0 < center_y + radius < self.canvas_height:
                continue
            if 0 < center_y - radius < self.canvas_height:
                break

        # Solution based on https://stackoverflow.com/a/23667813/15648632

        # Create index arrays to z
        I,J = np.meshgrid(np.arange(canvas.shape[0]),np.arange(canvas.shape[1]))

        # calculate distance of all points to centre
        dist = np.sqrt((I-center_x)**2+(J-center_y)**2)

        # Fill circle figure
        canvas[np.where(dist < radius)] = 1
        canvas[center_y+radius, center_x] = 1
        canvas[center_y-radius, center_x] = 1
        canvas[center_y, center_x+radius] = 1
        canvas[center_y, center_x-radius] = 1

        return canvas

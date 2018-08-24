import os
import numpy as np

path = os.getcwd()
src = os.path.join(path, 'src')


def get_colored_matrix(x, y):
    return np.array([[[(row + col) % x, col % y, row % x] for col in range(y)]
                     for row in range(x)])


def generate_one_color_matrix(x, y, pixel):
    return np.array([[pixel for _ in range(y)] for _ in range(x)])

import unittest
import convert
import numpy as np
from matplotlib import pyplot
import os

path = os.getcwd()


def get_colored_matrix(x, y):
    return np.array([[[row % 255, col % 255, (row+col) % 255] for col in range(y)] for row in range(x)])


def generate_one_color_matrix(x, y, pixel):
    return np.array([[pixel for i in range(y)]for j in range(x)])

class Test_get_bitmap_from_bmp(unittest.TestCase):

    def test_whiteImage_getAllWhite(self):
        test_matrix = generate_one_color_matrix(
            8**3, 8**3, [255, 255, 255])
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "white.bmp")),
            test_matrix)

    def test_BlackImage_getAllWhite(self):
        test_matrix = generate_one_color_matrix(
            8**3, 8**3, [0, 0, 0])
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "black.bmp")),
            test_matrix)

    def test_ColoredImage_getAllWhite(self):
        test_matrix = get_colored_matrix(255, 255)
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "colored.bmp")),
            test_matrix)


if __name__ == "__main__":
    unittest.main()

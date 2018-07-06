import unittest
import convert
import numpy as np
from matplotlib import pyplot
import os

path = os.getcwd()


class Test_get_bitmap_from_bmp(unittest.TestCase):

    @staticmethod
    def __generate_image_matrix(x, y, pixel):
        return np.array([[pixel for i in range(y)]for j in range(x)])

    @unittest.expectedFailure
    def test_whiteImage_getAllWhite(self):
        test_matrix = self.__generate_image_matrix(
            8**3, 8**3, [255, 255, 255])
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "white.bmp")),
            test_matrix)

    @unittest.expectedFailure
    def test_BlackImage_getAllWhite(self):
        test_matrix = self.__generate_image_matrix(
            8**3, 8**3, [0, 0, 0])
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "black.bmp")),
            test_matrix)


if __name__ == "__main__":
    unittest.main()

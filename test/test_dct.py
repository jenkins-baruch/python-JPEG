import unittest

from jpeg import dct
from test import *


class CaseDiscreteCosineTransform(unittest.TestCase):
    def test_discrete_cosine_transform(self):
        original = np.array([
            [52, 55, 61, 66, 70, 61, 64, 73],
            [63, 59, 55, 90, 109, 85, 69, 72],
            [62, 59, 68, 113, 144, 104, 66, 73],
            [63, 58, 71, 122, 154, 106, 70, 69],
            [67, 61, 68, 104, 126, 88, 68, 70],
            [79, 65, 60, 70, 77, 68, 58, 75],
            [85, 71, 64, 59, 55, 61, 65, 83],
            [87, 79, 69, 68, 65, 76, 78, 94]
        ])
        expected = np.array([
            [-415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46],
            [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88],
            [-46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65],
            [-48.53, 12.07, 34.10, -14.76, -10.24, 6.30, 1.83, 1.95],
            [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79, 3.14],
            [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
            [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
            [-0.17, 0.14, -1.07, -4.19, -1.17, -0.10, 0.50, 1.68]
        ])
        actual = dct.dct(original)

        max_different = np.max(np.abs(expected - actual))
        self.assertLessEqual(max_different, 0.01,
                             "There is different in size {} between expected and actual\n"
                             "expected:\n{}\nactual:\n{}".format(
                                 max_different, expected, actual))


class CaseQuantization(unittest.TestCase):
    @staticmethod
    def test_quantization():
        original = np.array([[
            -415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46
        ], [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88], [
            -46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65
        ], [-48.53, 12.07, 34.10, -14.76, -10.24, 6.30, 1.83,
            1.95], [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79,
                    3.14], [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
            [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
            [-0.17, 0.14, -1.07, -4.19, -1.17, -0.10, 0.50, 1.68]])
        expected = np.array([[-26, -3, -6, 2, 2, -1, 0, 0], [0, -2, -4, 1, 1, 0, 0, 0],
                             [-3, 1, 5, -1, -1, 0, 0, 0], [-3, 1, 2, -1, 0, 0, 0,
                                                           0], [1, 0, 0, 0, 0, 0, 0, 0],
                             [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0,
                                                        0], [0, 0, 0, 0, 0, 0, 0, 0]])
        actual = dct.quantization(original)

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class CaseUnQuantization(unittest.TestCase):
    @staticmethod
    def test_un_quantization():
        original = np.array([
            [-26, -3, -6, 2, 2, -1, 0, 0],
            [0, -2, -4, 1, 1, 0, 0, 0],
            [-3, 1, 5, -1, -1, 0, 0, 0],
            [-3, 1, 2, -1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        expected = np.array([
            [-416, -33, -60, 32, 48, -40, 0, 0],
            [0, -24, -56, 19, 26, 0, 0, 0],
            [-42, 13, 80, -24, -40, 0, 0, 0],
            [-42, 17, 44, -29, 0, 0, 0, 0],
            [18, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ])
        actual = dct.un_quantization(original)

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".format(original, actual, expected))


class CaseInverseDCT(unittest.TestCase):
    @staticmethod
    def test_inverse_DCT():
        original = [
            [-416, -33, -60, 32, 48, -40, 0, 0],
            [0, -24, -56, 19, 26, 0, 0, 0],
            [-42, 13, 80, -24, -40, 0, 0, 0],
            [-42, 17, 44, -29, 0, 0, 0, 0],
            [18, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
        expected = [
            [62, 65, 57, 60, 72, 63, 60, 82],
            [57, 55, 56, 82, 108, 87, 62, 71],
            [58, 50, 60, 111, 148, 114, 67, 65],
            [65, 55, 66, 120, 155, 114, 68, 70],
            [70, 63, 67, 101, 122, 88, 60, 78],
            [71, 71, 64, 70, 80, 62, 56, 81],
            [75, 82, 67, 54, 63, 65, 66, 83],
            [81, 94, 75, 54, 68, 81, 81, 87]
        ]
        actual = [[col for col in row]
                  for row in dct.inverse_dct(original)]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".format(original, actual, expected))

import unittest
import encode
import decode
import numpy as np
from matplotlib import pyplot
import os

path = os.getcwd()


def get_colored_matrix(x, y):
    return np.array([[[row % x, col % y, (row + col) % x]
                      for col in range(y)]
                     for row in range(x)])


def generate_one_color_matrix(x, y, pixel):
    return np.array([[pixel for i in range(y)] for j in range(x)])


class case_get_bitmap_from_bmp(unittest.TestCase):

    def test_whiteImage_getAllWhite(self):
        test_matrix = generate_one_color_matrix(8**3, 8**3, [255, 255, 255])
        np.testing.assert_array_equal(
            encode.get_bitmap_from_bmp(os.path.join("img", "white.bmp")),
            test_matrix)

    def test_BlackImage_getAllBlack(self):
        test_matrix = generate_one_color_matrix(8**3, 8**3, [0, 0, 0])
        np.testing.assert_array_equal(
            encode.get_bitmap_from_bmp(os.path.join("img", "black.bmp")),
            test_matrix)

    def test_ColoredImage_getAllColored(self):
        test_matrix = get_colored_matrix(255, 255)
        np.testing.assert_array_equal(
            encode.get_bitmap_from_bmp(os.path.join("img", "colored.bmp")),
            test_matrix)

    def test_NotProd8Size_ColoredImage(self):
        test_matrix = get_colored_matrix(100, 100)
        np.testing.assert_array_equal(
            encode.get_bitmap_from_bmp(
                os.path.join("img", "colored_100x100.bmp")), test_matrix)


class case_rgb_pixel_to_ycbcr(unittest.TestCase):

    def test_whitepixel(self):
        original = [255, 255, 255]
        expected = [255, 128, 128]
        actual = encode.rgb_pixel_to_ycbcr(*original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_blackpixel(self):
        original = [0, 0, 0]
        expected = [0, 128, 128]
        actual = encode.rgb_pixel_to_ycbcr(*original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_colorpixel(self):
        original = [48, 113, 219]  # #3071db Tchelet
        expected = [106, 192, 87]
        actual = encode.rgb_pixel_to_ycbcr(*original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_RGB_to_YCbCr(unittest.TestCase):

    def test_matrix(self):
        original = [[(255, 255, 255), (48, 113, 219),
                     (0, 0, 0)], [(0, 0, 0), (48, 113, 219), (255, 255, 255)],
                    [(48, 113, 219), (0, 0, 0), (0, 0, 0)],
                    [(255, 255, 255), (48, 113, 219), (255, 255, 255)]]
        expected = [[(255, 128, 128), (106, 192, 87), (0, 128, 128)],
                    [(0, 128, 128), (106, 192, 87), (255, 128, 128)],
                    [(106, 192, 87), (0, 128, 128),
                     (0, 128, 128)], [(255, 128, 128), (106, 192, 87),
                                      (255, 128, 128)]]
        actual = list(list(x) for x in encode.RGB_to_YCbCr(original))
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_YCbCr_Downstream(unittest.TestCase):

    def test_YCbCr_Downstream(self):
        original = [[(255, 255, 255), (0, 0, 0)], [(0, 0, 0), (48, 113, 219)],
                    [(48, 113, 219), (0, 0, 0)], [(255, 255, 255), (48, 113,
                                                                    219)]]
        expected = [[(255, 255, 255), (0, 255, 255)], [(0, 255, 255), (48, 255,
                                                                       255)],
                    [(48, 113, 219), (0, 113, 219)], [(255, 113, 219), (48, 113,
                                                                        219)]]
        actual = list(list(x) for x in encode.YCbCr_Downstream(original))
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_YCbCr_Downstream_odd(self):
        original = [[(255, 255, 255), (0, 0, 0),
                     (1, 2, 3)], [(0, 0, 0), (48, 113, 219), (4, 5, 6)],
                    [(48, 113, 219), (0, 0, 0), (7, 8, 9)]]
        expected = [[(255, 255, 255), (0, 255, 255),
                     (1, 2, 3)], [(0, 255, 255), (48, 255, 255), (4, 2, 3)],
                    [(48, 113, 219), (0, 113, 219), (7, 8, 9)]]
        actual = list(list(x) for x in encode.YCbCr_Downstream(original))
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_split_matrix_into_submatrixs(unittest.TestCase):

    def test_split_matrix_into_submatrixs(self):
        original = [[x * y for x in range(16)] for y in range(16)]
        expected = [[[x * y for x in range(8)] for y in range(8)],
                    [[x * y for x in range(8)] for y in range(8, 16)],
                    [[x * y for x in range(8, 16)] for y in range(8)],
                    [[x * y for x in range(8, 16)] for y in range(8, 16)]]
        actual = list(
            list(list(list(row)
                      for row in submatrix))
            for submatrix in encode.split_matrix_into_submatrixs(original))

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_split_matrix_into_submatrixs_odd(self):
        original = [[x * y for x in range(9)] for y in range(9)]
        expected = [[[x * y for x in range(8)] for y in range(8)],
                    [[x * y for x in range(8)] for y in range(8, 9)],
                    [[x * y for x in range(8, 9)] for y in range(8)],
                    [[x * y for x in range(8, 9)] for y in range(8, 9)]]
        actual = list(
            list(list(list(row)
                      for row in submatrix))
            for submatrix in encode.split_matrix_into_submatrixs(original))

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_centering_values_to_zero(unittest.TestCase):

    def test_centering_values_to_zero(self):
        original = [[[52, 55, 61], [66, 70, 61]], [[63, 59, 55], [90, 109, 85]],
                    [[62, 59, 68], [113, 144, 104]]]
        expected = [[[-76, -73, -67], [-62, -58, -67]],
                    [[-65, -69, -73], [-38, -19, -43]], [[-66, -69, -60],
                                                         [-15, 16, -24]]]
        actual = list(
            list(list(list(row)
                      for row in submatrix))
            for submatrix in encode.centering_values_to_zero(original))

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_discerete_cosine_transform(unittest.TestCase):

    def test_discerete_cosine_transform(self):
        original = [[-76, -73, -67, -62, -58, -67, -64,
                     -55], [-65, -69, -73, -38, -19, -43, -59,
                            -56], [-66, -69, -60, -15, 16, -24, -62,
                                   -55], [-65, -70, -57, -6, 26, -22, -58, -59],
                    [-61, -67, -60, -24, -2, -40, -60,
                     -58], [-49, -63, -68, -58, -51, -60, -70,
                            -53], [-43, -57, -64, -69, -73, -67, -63, -45],
                    [-41, -49, -59, -60, -63, -52, -50, -34]]
        expected = [[
            -415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46
        ], [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88], [
            -46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65
        ], [-48.53, 12.07, 34.10, -14.76, -10.24, 6.30, 1.83,
            1.95], [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79,
                    3.14], [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
                    [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
                    [-0.17, 0.14, -1.07, -4.19, -1.17, -0.10, 0.50, 1.68]]
        actual = [[col
                   for col in row]
                  for row in encode.discerete_cosine_transform(original)]

        np.testing.assert_array_almost_equal(
            expected,
            actual,
            decimal=2,
            err_msg=
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))
        # np.testing.assert_array_equal(
        #     expected, actual,
        #     "The original matrix- {} converted to {} and not to {} that expected"
        #     .format(original, actual, expected))


class case_quantization(unittest.TestCase):

    def test_quantization(self):
        original = [[
            -415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46
        ], [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88], [
            -46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65
        ], [-48.53, 12.07, 34.10, -14.76, -10.24, 6.30, 1.83,
            1.95], [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79,
                    3.14], [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
                    [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
                    [-0.17, 0.14, -1.07, -4.19, -1.17, -0.10, 0.50, 1.68]]
        expected = [[-26, -3, -6, 2, 2, -1, 0, 0], [0, -2, -4, 1, 1, 0, 0, 0],
                    [-3, 1, 5, -1, -1, 0, 0, 0], [-3, 1, 2, -1, 0, 0, 0,
                                                  0], [1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0,
                                               0], [0, 0, 0, 0, 0, 0, 0, 0]]
        actual = [[col for col in row] for row in encode.quantization(original)]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".
            format(original, actual, expected))


class case_un_quantization(unittest.TestCase):

    def test_un_quantization(self):
        original = [[-26, -3, -6, 2, 2, -1, 0, 0], [0, -2, -4, 1, 1, 0, 0, 0],
                    [-3, 1, 5, -1, -1, 0, 0, 0], [-3, 1, 2, -1, 0, 0, 0,
                                                  0], [1, 0, 0, 0, 0, 0, 0, 0]]
        expected = [[-416, -33, -60, 32, 48, -40, 0,
                     0], [0, -24, -56, 19, 26, 0, 0,
                          0], [-42, 13, 80, -24, -40, 0, 0, 0],
                    [-42, 17, 44, -29, 0, 0, 0, 0], [18, 0, 0, 0, 0, 0, 0, 0]]
        actual = [
            [col for col in row] for row in decode.un_quantization(original)
        ]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".
            format(original, actual, expected))

class case_inverse_DCT(unittest.TestCase):
    def test_inverse_DCT(self):
        original = [[-416, -33, -60, 32, 48, -40, 0,
                     0], [0, -24, -56, 19, 26, 0, 0,
                          0], [-42, 13, 80, -24, -40, 0, 0, 0],
                    [-42, 17, 44, -29, 0, 0, 0, 0],
                     [18, 0, 0, 0, 0, 0, 0, 0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0]
                     ]
        expected = [
            [-66,-63-71,-68,-56,-65,-68,-46],
            [-71,-73,-72,-46,-20,-41,-66,-57],
            [-70,-78,-68,-17,20,-14,-61,-63],
            [-63,-73,-62,-8,27,-14,-60,-58],
            [-58,-65,-61,-27,-6,-40,-68,-50],
            [-57,-57,-64,-58,-48,-66,-72,-47],
            [-53,-46,-61,-74,-65,-63,-62,-45],
            [-47,-34,-53,-74,-60,-47,-47,-41]
        ]
        actual = [
            [col for col in row] for row in decode.inverse_DCT(original)
        ]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".
            format(original, actual, expected))
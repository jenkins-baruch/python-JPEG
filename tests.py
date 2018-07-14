import unittest
import convert
import numpy as np
from matplotlib import pyplot
import os

path = os.getcwd()


def get_colored_matrix(x, y):
    return np.array([[[row % x, col % y, (row + col) % x] for col in range(y)]
                     for row in range(x)])


def generate_one_color_matrix(x, y, pixel):
    return np.array([[pixel for i in range(y)] for j in range(x)])


class case_get_bitmap_from_bmp(unittest.TestCase):
    def test_whiteImage_getAllWhite(self):
        test_matrix = generate_one_color_matrix(8**3, 8**3, [255, 255, 255])
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "white.bmp")),
            test_matrix)

    def test_BlackImage_getAllBlack(self):
        test_matrix = generate_one_color_matrix(8**3, 8**3, [0, 0, 0])
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "black.bmp")),
            test_matrix)

    def test_ColoredImage_getAllColored(self):
        test_matrix = get_colored_matrix(255, 255)
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(os.path.join("img", "colored.bmp")),
            test_matrix)

    def test_NotProd8Size_ColoredImage(self):
        test_matrix = get_colored_matrix(100, 100)
        np.testing.assert_array_equal(
            convert.get_bitmap_from_bmp(
                os.path.join("img", "colored_100x100.bmp")), test_matrix)


class case_rgb_pixel_to_ycbcr(unittest.TestCase):
    def test_whitepixel(self):
        original = [255, 255, 255]
        expected = [255, 128, 128]
        actual = convert.rgb_pixel_to_ycbcr(*original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_blackpixel(self):
        original = [0, 0, 0]
        expected = [0, 128, 128]
        actual = convert.rgb_pixel_to_ycbcr(*original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_colorpixel(self):
        original = [48, 113, 219]  # #3071db Tchelet
        expected = [106, 192, 87]
        actual = convert.rgb_pixel_to_ycbcr(*original)
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
        actual = list(list(x) for x in convert.RGB_to_YCbCr(original))
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_YCbCr_Downstream(unittest.TestCase):
    def test_YCbCr_Downstream(self):
        original = [[(255, 255, 255), (0, 0, 0)], [
            (0, 0, 0),
            (48, 113, 219),
        ], [(48, 113, 219), (0, 0, 0)], [(255, 255, 255), (48, 113, 219)]]
        expected = [[(255, 255, 255), (0, 255, 255)], [
            (0, 255, 255),
            (48, 255, 255),
        ], [(48, 113, 219), (0, 113, 219)], [(255, 113, 219), (48, 113, 219)]]
        actual = list(list(x) for x in convert.YCbCr_Downstream(original))
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
        actual = list(list(x) for x in convert.YCbCr_Downstream(original))
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_split_matrix_into_submatrixs(unittest.TestCase):
    def test_split_matrix_into_submatrixs(self):
        original = [[x*y for x in range(16)] for y in range(16)]
        expected = [
            [[x*y for x in range(8)] for y in range(8)],
            [[x*y for x in range(8)] for y in range(8, 16)],
            [[x*y for x in range(8, 16)] for y in range(8)],
            [[x*y for x in range(8, 16)] for y in range(8, 16)]
        ]
        actual = list(
            list(
                list(list(row) for row in submatrix)
            ) for submatrix in convert.split_matrix_into_submatrixs(original)
        )

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_split_matrix_into_submatrixs_odd(self):
        original = [[x*y for x in range(9)] for y in range(9)]
        expected = [
            [[x*y for x in range(8)] for y in range(8)],
            [[x*y for x in range(8)] for y in range(8, 9)],
            [[x*y for x in range(8, 9)] for y in range(8)],
            [[x*y for x in range(8, 9)] for y in range(8, 9)]
        ]
        actual = list(
            list(
                list(list(row) for row in submatrix)
            ) for submatrix in convert.split_matrix_into_submatrixs(original)
        )

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


if __name__ == "__main__":
    unittest.main()

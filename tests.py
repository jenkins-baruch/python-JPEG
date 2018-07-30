import unittest
import encode
import dct
import numpy as np
from matplotlib import pyplot
import os
import entropy

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
        actual = encode.rgb_pixel_to_ycbcr(original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_blackpixel(self):
        original = [0, 0, 0]
        expected = [0, 128, 128]
        actual = encode.rgb_pixel_to_ycbcr(original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_colorpixel(self):
        original = [48, 113, 219]  # #3071db Tchelet
        expected = [106, 192, 87]
        actual = encode.rgb_pixel_to_ycbcr(original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_RGB_to_YCbCr(unittest.TestCase):
    def test_matrix(self):
        original = [
            [(255, 255, 255), (48, 113, 219), (0, 0, 0)],
            [(0, 0, 0), (48, 113, 219), (255, 255, 255)],
            [(48, 113, 219), (0, 0, 0), (0, 0, 0)],
            [(255, 255, 255), (48, 113, 219), (255, 255, 255)]
        ]
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


class case_YCbCr_Downsample(unittest.TestCase):
    def test_YCbCr_Downsample(self):
        original = np.array([
            [150, 2, 255, 100],
            [123,234,23,34],
            [65,87,234,166],
            [68,253,0,165]
        ])
        expected = [
            [150, 255],
            [65,234]
        ]
        actual = encode.YCbCr_Downsample(original)
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_YCbCr_Downsample_odd(self):
        original = np.array([
            [150, 2, 255, 100, 89],
            [123,234,23,34, 0],
            [65,87,234,166, 176],
            [68,253,0,165, 56],
            [57,10,187,34,76]
        ])
        expected = [
            [150,255,89],
            [65,234,176],
            [57,187,76]
        ]
        actual = encode.YCbCr_Downsample(original)
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

class case_seperate_y_cb_cr(unittest.TestCase):
    def test_seperate_y_cb_cr(self):
        original = np.array([
            [[52, 55, 61], [66, 70, 61]],
            [[63, 59, 55], [90, 109, 85]],
            [[62, 59, 68], [113, 144, 104]]
        ])
        expected = [
            [
                [52,66],
                [63,90],
                [62,113]
            ],
            [
                [55,70],
                [59,109],
                [59,144]
            ],
            [
                [61,61],
                [55,85],
                [68,104]
            ]
        ]
        y, cb, cr = encode.seperate_y_cb_cr(original)
        actual = [
            [[cell for cell in row] for row in y],
            [[cell for cell in row] for row in cb],
            [[cell for cell in row] for row in cr]
        ]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

class case_split_matrix_into_submatrixs(unittest.TestCase):
    def test_split_matrix_into_submatrixs(self):
        original = [
            [x * y for x in range(16)]
             for y in range(16)
        ]
        expected = [
            [
                [x * y for x in range(8)] for y in range(8)
            ],
            [
                [x * y for x in range(8)] for y in range(8, 16)
            ],
            [
                [x * y for x in range(8, 16)] for y in range(8)
            ],
            [
                [x * y for x in range(8, 16)] for y in range(8, 16)
            ]
        ]
        actual = encode.split_matrix_into_submatrixs(original)

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
            list(list(list(row) for row in submatrix))
            for submatrix in encode.split_matrix_into_submatrixs(original))

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

class case_padding_matrix_to_8_8(unittest.TestCase):
    def test_padding_matrix_to_8_8(self):
        original = np.array([
            [-76, -73],
            [-65, -69],
            [-66, -69],
            [-65, -70],
            [-61, -67]
        ])
        expected = np.array([
            [-76, -73, 0, 0, 0, 0, 0, 0],
            [-65, -69, 0, 0, 0, 0, 0, 0],
            [-66, -69, 0, 0, 0, 0, 0, 0],
            [-65, -70, 0, 0, 0, 0, 0, 0],
            [-61, -67, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0,
                0, 0, 0, 0],
            [0, 0, 0, 0,
                0, 0, 0, 0],
            [0, 0, 0, 0,
                0, 0, 0, 0]
        ])
        actual = encode.padding_matrix_to_8_8(original)

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class case_discerete_cosine_transform(unittest.TestCase):
    def test_discerete_cosine_transform(self):
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
        expected = [[
            -415.38, -30.19, -61.20, 27.24, 56.12, -20.10, -2.39, 0.46
        ], [4.47, -21.86, -60.76, 10.25, 13.15, -7.09, -8.54, 4.88], [
            -46.83, 7.37, 77.13, -24.56, -28.91, 9.93, 5.42, -5.65
        ], [-48.53, 12.07, 34.10, -14.76, -10.24, 6.30, 1.83,
            1.95], [12.12, -6.55, -13.20, -3.95, -1.87, 1.75, -2.79,
                    3.14], [-7.73, 2.91, 2.38, -5.94, -2.38, 0.94, 4.30, 1.85],
            [-1.03, 0.18, 0.42, -2.42, -0.88, -3.02, 4.12, -0.66],
            [-0.17, 0.14, -1.07, -4.19, -1.17, -0.10, 0.50, 1.68]]
        actual = [[col for col in row]
                  for row in dct.DCT(original)]

        np.testing.assert_array_almost_equal(
            expected,
            actual,
            decimal=2,
            err_msg="The original matrix- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


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
        actual = [[col for col in row]
                  for row in dct.quantization(original)]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".
            format(original, actual, expected))


class case_un_quantization(unittest.TestCase):
    def test_un_quantization(self):
        original = [
            [-26, -3, -6, 2, 2, -1, 0, 0],
            [0, -2, -4, 1, 1, 0, 0, 0],
            [-3, 1, 5, -1, -1, 0, 0, 0],
            [-3, 1, 2, -1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0]
        ]
        expected = [
            [-416, -33, -60, 32, 48, -40, 0, 0],
            [0, -24, -56, 19, 26, 0, 0, 0],
            [-42, 13, 80, -24, -40, 0, 0, 0],
            [-42, 17, 44, -29, 0, 0, 0, 0],
            [18, 0, 0, 0, 0, 0, 0, 0]
        ]
        actual = [[col for col in row]
                  for row in dct.un_quantization(original)]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".
            format(original, actual, expected))


class case_inverse_DCT(unittest.TestCase):
    def test_inverse_DCT(self):
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
                  for row in dct.inverse_DCT(original)]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".
            format(original, actual, expected))

class case_entropy(unittest.TestCase):
    def test_entropy(self):
        words = [
            "love","love","love","love",
            "wave","wave","wave","wave"
        ]
        original = np.array([list(word) for word in words])
        expected = 2.5
        actual = entropy.entropy(original)
        self.assertAlmostEqual(expected, actual)
    
    def test_entropy_2(self):
        original =np.array([
            [12,15,22,8,4,4,4,4,4,4,4,4,4,4,4,4],
            [23,6,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
        ])
        expected = 1.18
        actual = entropy.entropy(original)
        self.assertAlmostEqual(expected, actual, places=2)

class case_concatenate_submatrixes_to_big_matrix(unittest.TestCase):
    def test_concatenate_submatrixes_to_big_matrix_tiny(self):
        original = [
            np.array([
                [1,1],
                [1,1]
            ]),
            np.array([
                [2,2],
                [2,2]
            ]),
            np.array([
                [3,3],
                [3,3]
            ]),
            np.array([
                [4,4],
                [4,4]
            ])
        ]
        expected = np.array([
            [1,1,2,2],
            [1,1,2,2],
            [3,3,4,4],
            [3,3,4,4]
        ])
        actual = encode.concatenate_submatrixes_to_big_matrix(original, (2,2))
        np.testing.assert_array_equal(expected, actual)

    def test_concatenate_submatrixes_to_big_matrix_odd_shape(self):
        original = [
            np.array([
                [1,1],
                [1,1]
            ]),
            np.array([
                [2,2],
                [2,2]
            ]),
            np.array([
                [3,3],
                [3,3]
            ]),
            np.array([
                [4,4],
                [4,4]
            ]),
            np.array([
                [5,5],
                [5,5]
            ]),
            np.array([
                [6,6],
                [6,6]
            ])
        ]
        expected = np.array([
            [1,1,2,2,3,3],
            [1,1,2,2,3,3],
            [4,4,5,5,6,6],
            [4,4,5,5,6,6]
        ])
        actual = encode.concatenate_submatrixes_to_big_matrix(original, (3,2))
        np.testing.assert_array_equal(expected, actual)

class case_concatenate_Y_Cb_Cr(unittest.TestCase):
    def test_concatenate_Y_Cb_Cr(self):
        original = [
            np.array([
                [1,2,3],
                [4,5,6],
                [7,8,9]
            ]),
            np.array([
                [7,8,9],
                [1,2,3],
                [4,5,6]
            ]),
            np.array([
                [4,5,6],
                [7,8,9],
                [1,2,3]
            ])
        ]
        expected = np.array([
            [[1,7,4],[2,8,5],[3,9,6]],
            [[4,1,7],[5,2,8],[6,3,9]],
            [[7,4,1],[8,5,2],[9,6,3]]
        ])
        actual = encode.concatenate_Y_Cb_Cr(*original)
        np.testing.assert_array_equal(expected,actual)

class case_main(unittest.TestCase):
    def test_main(self):
        self.assertEqual(1,encode.main("img/colored.bmp"))
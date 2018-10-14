import unittest

import numpy as np

from jpeg import encode


class CaseYCrCbDownsample(unittest.TestCase):
    @staticmethod
    def test_YCrCb_Downsample():
        original = np.array([
            [150, 2, 255, 100],
            [123, 234, 23, 34],
            [65, 87, 234, 166],
            [68, 253, 0, 165]
        ])
        expected = [
            [150, 255],
            [65, 234]
        ]
        actual = encode.downsample(original)
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected".format(original, actual, expected))

    @staticmethod
    def test_YCrCb_Downsample_odd():
        original = np.array([
            [150, 2, 255, 100, 89],
            [123, 234, 23, 34, 0],
            [65, 87, 234, 166, 176],
            [68, 253, 0, 165, 56],
            [57, 10, 187, 34, 76]
        ])
        expected = [
            [150, 255, 89],
            [65, 234, 176],
            [57, 187, 76]
        ]
        actual = encode.downsample(original)
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected".format(original, actual, expected))


class CaseUpsample(unittest.TestCase):
    @staticmethod
    def test_upsample():
        original = np.array([
            [150, 255],
            [65, 234]
        ])
        expected = np.array([
            [150, 150, 255, 255],
            [150, 150, 255, 255],
            [65, 65, 234, 234],
            [65, 65, 234, 234]
        ])
        actual = encode.upsample(original)
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected".format(original, actual, expected))


class CaseSplitToThreeColors(unittest.TestCase):
    @staticmethod
    def test_split_y_cb_cr():
        original = np.array([
            [[52, 55, 61], [66, 70, 61]],
            [[63, 59, 55], [90, 109, 85]],
            [[62, 59, 68], [113, 144, 104]]
        ])
        expected = [
            [
                [52, 66],
                [63, 90],
                [62, 113]
            ],
            [
                [55, 70],
                [59, 109],
                [59, 144]
            ],
            [
                [61, 61],
                [55, 85],
                [68, 104]
            ]
        ]
        y, cb, cr = encode.split_to_three_colors(original)
        actual = [
            [[cell for cell in row] for row in y],
            [[cell for cell in row] for row in cb],
            [[cell for cell in row] for row in cr]
        ]

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".format(original, actual, expected))


class CaseSplitMatrixIntoSubmatrices(unittest.TestCase):
    @staticmethod
    def test_split_matrix_into_submatrices():
        original = np.array([
            [x * y for x in range(16)]
            for y in range(16)
        ])
        expected = [
            [
                [x * y for x in range(8)] for y in range(8)
            ],
            [
                [x * y for x in range(8, 16)] for y in range(8)
            ],
            [
                [x * y for x in range(8)] for y in range(8, 16)
            ],
            [
                [x * y for x in range(8, 16)] for y in range(8, 16)
            ]
        ]
        actual = encode.split_matrix_into_sub_matrices(original)

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".format(original, actual, expected))

    @staticmethod
    @unittest.skip('All matrices should be in size divided by 8 (or 16, 32)')
    def test_split_matrix_into_submatrices_odd():
        original = np.array([[x * y for x in range(9)] for y in range(9)])
        expected = [[[x * y for x in range(8)] for y in range(8)],
                    [[x * y for x in range(8, 9)] for y in range(8)],
                    [[x * y for x in range(8)] for y in range(8, 9)],
                    [[x * y for x in range(8, 9)] for y in range(8, 9)]]
        actual = list(
            list(list(list(row) for row in submatrix))
            for submatrix in encode.split_matrix_into_sub_matrices(original))

        np.testing.assert_array_equal(
            expected, actual,
            "The original matrix- {} converted to {} and not to {} that expected".format(original, actual, expected))


class CaseConcatenateSubmatricesToBigMatrix(unittest.TestCase):
    @staticmethod
    def test_concatenate_submatrices_to_big_matrix_tiny():
        original = [
            np.array([
                [1, 1],
                [1, 1]
            ]),
            np.array([
                [2, 2],
                [2, 2]
            ]),
            np.array([
                [3, 3],
                [3, 3]
            ]),
            np.array([
                [4, 4],
                [4, 4]
            ])
        ]
        expected = np.array([
            [1, 1, 2, 2],
            [1, 1, 2, 2],
            [3, 3, 4, 4],
            [3, 3, 4, 4]
        ])
        actual = encode.concatenate_sub_matrices_to_big_matrix(original, (2, 2))
        np.testing.assert_array_equal(expected, actual)

    @staticmethod
    def test_concatenate_submatrices_to_big_matrix_odd_shape():
        original = [
            np.array([
                [1, 1],
                [1, 1]
            ]),
            np.array([
                [2, 2],
                [2, 2]
            ]),
            np.array([
                [3, 3],
                [3, 3]
            ]),
            np.array([
                [4, 4],
                [4, 4]
            ]),
            np.array([
                [5, 5],
                [5, 5]
            ]),
            np.array([
                [6, 6],
                [6, 6]
            ])
        ]
        expected = np.array([
            [1, 1, 2, 2, 3, 3],
            [1, 1, 2, 2, 3, 3],
            [4, 4, 5, 5, 6, 6],
            [4, 4, 5, 5, 6, 6]
        ])
        actual = encode.concatenate_sub_matrices_to_big_matrix(original, (2, 3))
        np.testing.assert_array_equal(expected, actual)


class CaseConcatenateColors(unittest.TestCase):
    @staticmethod
    def test_concatenate_Y_Cr_Cb():
        original = [
            np.array([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]
            ]),
            np.array([
                [7, 8, 9],
                [1, 2, 3],
                [4, 5, 6]
            ]),
            np.array([
                [4, 5, 6],
                [7, 8, 9],
                [1, 2, 3]
            ])
        ]
        expected = np.array([
            [[1, 7, 4], [2, 8, 5], [3, 9, 6]],
            [[4, 1, 7], [5, 2, 8], [6, 3, 9]],
            [[7, 4, 1], [8, 5, 2], [9, 6, 3]]
        ])
        actual = encode.concatenate_three_colors(*original)
        np.testing.assert_array_equal(expected, actual)


class CaseShapeForContacting(unittest.TestCase):
    def test_shape_for_contacting(self):
        original = (9, 10)
        excepted = (2, 2)
        actual = encode.shape_for_contacting(original)
        self.assertEqual(excepted, actual)


class CaseCropBitmap(unittest.TestCase):
    @staticmethod
    def test_crop_bitmap():
        original = np.array([
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 5, 6, 7, 8, 9]
        ])
        excepted = np.array([
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
            [1, 2, 3, 4, 5, 6, 7, 8],
        ])
        actual = encode.crop_bitmap(original)
        np.testing.assert_array_equal(excepted, actual)

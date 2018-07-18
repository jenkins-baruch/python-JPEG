import sys
import math
import numpy as np
from PIL import Image
from matplotlib import image, pyplot


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return image.imread(path)


def rgb_pixel_to_ycbcr(r: int, g: int, b: int):
    return [
        int(round(0 + .299 * r + .587 * g + .114 * b)),  # Y'
        int(round(128 - .168736 * r - .331264 * g + .5 * b)),  # Cb
        int(round(128 + .5 * r - .418688 * g - .081312 * b))  # Cr
    ]


def RGB_to_YCbCr(matrix):
    """Converting pixels from RGB (Red, Green, Blue) to YCbCr (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCbCr as 2D array
    """
    return ((rgb_pixel_to_ycbcr(col[0], col[1], col[2])
             for col in row)
            for row in matrix)


def YCbCr_Downstream(matrix):
    """Downstream the Cb and Cr with 4:2:0 correlation

    Arguments:
        matrix {ndarray} -- The image matrix as YCbCr

    Returns:
        ndarray -- The new image matrix with downstreamed YCbCr
    """
    return (
        (
            [
                matrix[j][i][0],  # Y
                matrix[j - j % 2][i - i % 2][1],  # Cb downstream
                matrix[j - j % 2][i - i % 2][2]  # Cr downstrem
            ] for i in range(len(matrix[j]))  # index in row
        ) for j in range(len(matrix))  # index in column
    )


def split_matrix_into_submatrixs(matrix):
    """Split the bitmap to 8*8 matrixs

    Arguments:
        matrix {ndarray} -- The image bitmap

    Returns:
        list -- list of all 8*8 ndarrays matrix
    """
    return (
        (
            ((matrix[row_index][col_index]
              for col_index in range(col, min(col + 8, len(matrix[0]))))
             )  # row in matrix
            for row_index in range(row, min(row + 8, len(matrix)))
        )  # 8*8 matrix
        for col in range(0, len(matrix[0]), 8)
        for row in range(0, len(matrix), 8))


def centering_values_to_zero(submatrix):
    """Normalize YCbCr values- remove 128 from each object

    Arguments:
        submatrix {ndarray} -- 8*8 Submatrix

    Returns:
        ndarray -- 8*8 normalized submatrix
    """
    return (([col[0] - 128, col[1] - 128, col[2] - 128]
             for col in row)
            for row in submatrix)


def __alpha(u):
    return 1 / math.sqrt(2) if u == 0 else 1


def __G_uv(u, v, matrix):
    return (1 / 4) * __alpha(u) * __alpha(v) * sum(
        matrix[x][y] * math.cos((2 * x + 1) * u * math.pi / 16) * math.cos(
            (2 * y + 1) * v * math.pi / 16)
        for x in range(len(matrix))
        for y in range(len(matrix[0])))


def discerete_cosine_transform(matrix):
    return ((round(__G_uv(y, x, matrix), 2)
             for x in range(len(matrix[y])))
            for y in range(len(matrix)))


def quantization(submatrix):
    q = [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]
    return (
        (round(submatrix[row][col]/q[row][col])
         for col in range(len(submatrix[row])))
        for row in range(len(submatrix))
    )


if __name__ == "__main__":
    get_bitmap_from_bmp(sys.argv[0])

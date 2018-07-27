import sys
import math
import dct
import numpy as np
from PIL import Image
from matplotlib import image, pyplot
import itertools


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return image.imread(path)


def rgb_pixel_to_ycbcr(r: int, g: int, b: int):
    return [
        int(round(0 + .299 * r + .587 * g + .114 * b)),  # Y'
        int(round(128 - .168736 * r - .331264 * g + .5 * b)),  # Cb
        int(round(128 + .5 * r - .418688 * g - .081312 * b))  # Cr
    ]


def RGB_to_YCbCr(matrix3D):
    """Converting pixels from RGB (Red, Green, Blue) to YCbCr (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCbCr as 2D array
    """
    return [[rgb_pixel_to_ycbcr(col[0], col[1], col[2])
             for col in row]
            for row in matrix3D]

def seperate_y_cb_cr(YCbCr_matrix):
    return [[cell[0] for cell in row] for row in YCbCr_matrix], [[cell[1] for cell in row] for row in YCbCr_matrix], [[cell[2] for cell in row] for row in YCbCr_matrix]

def YCbCr_Downsample(matrix):
    return [row[::2] for row in matrix[::2]]


def split_matrix_into_submatrixs(matrix:list):
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


def average(matrix):
    return round(
        sum(
            (sum(cell for cell in row))
            for row in matrix) /
        (len(matrix)*len(matrix[0]))
    )


def padding_matrix_to_8_8(matrix):
    return (
        (
            matrix[row][col]
            if col < len(matrix[0]) and row < len(matrix)
            else average(matrix)
            for col in range(8)
        )
        for row in range(8)
    )


def compress_image(path):
    print("Reading file")
    bitmap = get_bitmap_from_bmp(path)

    print("Converting to YCbCr")
    ycbcr_bitmap = RGB_to_YCbCr(bitmap)

    print("Seperating bitmap to Y, Cb, Cr matrixes")
    y, cb, cr = seperate_y_cb_cr(ycbcr_bitmap)
    
    print("Downsampling")
    cb_downsample = YCbCr_Downsample(cb)
    cr_downsample = YCbCr_Downsample(cr)
    
    print("Splitting to 8x8 submatrixes")
    y_split = split_matrix_into_submatrixs(y)
    cb_split = split_matrix_into_submatrixs(cb_downsample)
    cr_split = split_matrix_into_submatrixs(cr_downsample)

    print("DCT")
    y_dct = (dct.DCT(padding_matrix_to_8_8(submatrix)) for submatrix in y_split)
    cb_dct = (dct.DCT(padding_matrix_to_8_8(submatrix)) for submatrix in cb_split)
    cr_dct = (dct.DCT(padding_matrix_to_8_8(submatrix)) for submatrix in cr_split)

    print("Quantization")
    y_quantization = (dct.quantization(submatrix) for submatrix in y_dct)
    cb_quantization = (dct.quantization(submatrix) for submatrix in cb_dct)
    cr_quantization = (dct.quantization(submatrix) for submatrix in cr_dct)

if __name__ == "__main__":
    import argparse
    from pyfiglet import Figlet

    # fonts from http://www.figlet.org/examples.html
    print(Figlet(font='alligator').renderText('J P E G'))
    print(Figlet(font='big').renderText('By'))
    print(Figlet(font='colossal').renderText('Meny'))
    print(Figlet(font='colossal').renderText('Baruch'))
    print(Figlet(font='colossal').renderText('L i t a l'))

    parser = argparse.ArgumentParser(
        description='Compress image by JPEG algorithm')
    parser.add_argument('PATH')
    args = parser.parse_args()
    print(args.PATH)
    compress_image(args.PATH)

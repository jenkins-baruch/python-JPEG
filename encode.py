import sys
import math
import dct
import numpy as np
from PIL import Image
from matplotlib import image, pyplot
import itertools
import entropy as ent


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return image.imread(path)


def rgb_pixel_to_ycbcr(rgb: list)->[int, int, int]:
    return [
        int(round(0 + .299 * rgb[0] + .587 * rgb[1] + .114 * rgb[2])),  # Y'
        int(round(128 - .168736 * rgb[0] - .331264 * rgb[1] + .5 * rgb[2])),  # Cb
        int(round(128 + .5 * rgb[0] - .418688 * rgb[1] - .081312 * rgb[2]))  # Cr
    ]

    
def RGB_to_YCbCr(matrix3D:np.ndarray)->np.ndarray:
    """Converting pixels from RGB (Red, Green, Blue) to YCbCr (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCbCr as 2D array
    """
    return np.apply_along_axis(rgb_pixel_to_ycbcr, 2, matrix3D)

def seperate_y_cb_cr(YCbCr_matrix:np.ndarray):
    return [YCbCr_matrix[...,0], YCbCr_matrix[...,1], YCbCr_matrix[...,2]]
    # [[cell[0] for cell in row] for row in YCbCr_matrix], [[cell[1] for cell in row] for row in YCbCr_matrix], [[cell[2] for cell in row] for row in YCbCr_matrix]

def YCbCr_Downsample(matrix):
    return [row[::2] for row in matrix[::2]]

def CbCr_Upsample(matrix:np.ndarray)->np.ndarray:
    return matrix.repeat(2, axis=0).repeat(2, axis=1)


def split_matrix_into_submatrixs(matrix:list):
    """Split the bitmap to 8*8 matrixs

    Arguments:
        matrix {ndarray} -- The image bitmap

    Returns:
        list -- list of all 8*8 ndarrays matrix
    """
    return [
        [
            [matrix[row_index][col_index]
              for col_index in range(col, min(col + 8, len(matrix[0])))
            ]  # row in matrix
            for row_index in range(row, min(row + 8, len(matrix)))
        ]  # 8*8 matrix
        for col in range(0, len(matrix[0]), 8)
        for row in range(0, len(matrix), 8)]


def average(matrix):
    return round(
        sum(
            (sum(cell for cell in row))
            for row in matrix) /
        (len(matrix)*len(matrix[0]))
    )


def padding_matrix_to_8_8(matrix):
    return [
        [
            matrix[row][col]
            if col < len(matrix[0]) and row < len(matrix)
            else average(matrix)
            for col in range(8)
        ]
        for row in range(8)
    ]


def compress_image(path, entropy=False):
    print("Reading file")
    bitmap = get_bitmap_from_bmp(path)

    if entropy:
        print("Bitmap entropy: " + str(ent.entropy(bitmap)))

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

    print("paddings")

    print("DCT")
    y_dct = [dct.DCT(padding_matrix_to_8_8(submatrix)) for submatrix in y_split]
    cb_dct = [dct.DCT(padding_matrix_to_8_8(submatrix)) for submatrix in cb_split]
    cr_dct = [dct.DCT(padding_matrix_to_8_8(submatrix)) for submatrix in cr_split]

    print("Quantization")
    y_quantization = [dct.quantization(submatrix) for submatrix in y_dct]
    cb_quantization = [dct.quantization(submatrix) for submatrix in cb_dct]
    cr_quantization = [dct.quantization(submatrix) for submatrix in cr_dct]

    if entropy:
        print("Compressed entropy: " + str(ent.entropy(np.array([y_quantization, cb_quantization, cr_quantization]))))
    
    y_un_quantization = [dct.un_quantization(submatrix) for submatrix in y_quantization]
    cb_un_quantization = [dct.un_quantization(submatrix) for submatrix in cb_quantization]
    cr_un_quantization = [dct.un_quantization(submatrix) for submatrix in cr_quantization]

    y_invert_dct = [dct.inverse_DCT(matrix) for matrix in y_un_quantization]
    cb_invert_dct = [dct.inverse_DCT(matrix) for matrix in cb_un_quantization]
    cr_invert_dct = [dct.inverse_DCT(matrix) for matrix in cr_un_quantization]


    
def main(*argv):
    import argparse
    import imghdr
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
    parser.add_argument('-e', action='store_true', help='Show entropy of images')
    args = parser.parse_args()
    if imghdr.what(args.PATH) != 'bmp':
        print("{} format is not supported for now".format(imghdr.what(args.PATH)), file=sys.stderr)
    else:
        compress_image(args.PATH, args.e)

if __name__ == "__main__":
    main(sys.argv)

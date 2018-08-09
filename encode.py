import sys
import math
import dct
import numpy as np
from PIL import Image
import itertools
import entropy as ent
from typing import List, Tuple
import imagetools


def rgb_pixel_to_ycbcr(rgb: list)->List[int]:
    return [
        np.uint8(0 + (0.299 * rgb[0]) +
                 (0.587 * rgb[1]) + (0.114 * rgb[2])),  # Y'
        np.uint8(128 - (0.168736 * rgb[0]) - \
                 (0.331264 * rgb[1]) + (0.5 * rgb[2])),  # Cb
        np.uint8(128 + (0.5 * rgb[0]) - (0.418688 * \
                                         rgb[1]) - (0.081312 * rgb[2]))  # Cr
    ]


def RGB_to_YCbCr(matrix3D: np.ndarray)->np.ndarray:
    """Converting pixels from RGB (Red, Green, Blue) to YCbCr (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCbCr as 2D array
    """
    return np.apply_along_axis(rgb_pixel_to_ycbcr, 2, matrix3D)


def seperate_y_cb_cr(YCbCr_matrix: np.ndarray)->List[np.ndarray]:
    return [YCbCr_matrix[..., 0], YCbCr_matrix[..., 1], YCbCr_matrix[..., 2]]


def YCbCr_Downsample(matrix: np.ndarray):
    return matrix[::2, ::2]


def CbCr_Upsample(matrix: np.ndarray)->np.ndarray:
    return matrix.repeat(2, axis=0).repeat(2, axis=1)


def split_matrix_into_submatrixs(matrix: np.ndarray)->List[np.ndarray]:
    """Split the bitmap to 8*8 matrixs

    Arguments:
        matrix {ndarray} -- The image bitmap

    Returns:
        list -- list of all 8*8 ndarrays matrix
    """
    return [
        np.array([
            [matrix[row_index][col_index]
             for col_index in range(col, min(col + 8, len(matrix[0])))
             ]  # row in matrix
            for row_index in range(row, min(row + 8, len(matrix)))
        ])  # 8*8 matrix
        for col in range(0, len(matrix[0]), 8)
        for row in range(0, len(matrix), 8)]


def padding_matrix_to_8_8(matrix: np.ndarray)->np.ndarray:
    return np.pad(matrix, ((0, 8-matrix.shape[0]), (0, 8-matrix.shape[1])), 'constant')


def concatenate_submatrixes_to_big_matrix(submatrixes: List[np.ndarray], shape: Tuple[int]):
    return np.block([submatrixes[i:i+shape[0]] for i in range(0, len(submatrixes), shape[0])])


def concatenate_Y_Cb_Cr(Y: np.ndarray, Cb: np.ndarray, Cr: np.ndarray)->np.ndarray:
    return np.dstack((Y, Cb, Cr))


def compress_image(path, entropy=False):    # pragma: no cover
    print("Reading file")
    bitmap = imagetools.get_bitmap_from_bmp(path)
    
    if entropy:
        print("Bitmap entropy: " + str(ent.entropy(bitmap)))

    print("Converting to YCbCr")
    ycbcr_bitmap = RGB_to_YCbCr(bitmap)

    print("Seperating bitmap to Y, Cb, Cr matrixes")
    y, cb, cr = seperate_y_cb_cr(ycbcr_bitmap)

    print("Downsampling")
    cb_downsample = YCbCr_Downsample(cb)
    cr_downsample = YCbCr_Downsample(cr)

    y_shape = (math.ceil(y.shape[0]/8), math.ceil(y.shape[1]/8))
    cb_shape = (
        math.ceil(cb_downsample.shape[0]/8), math.ceil(cb_downsample.shape[1]/8))
    cr_shape = (
        math.ceil(cr_downsample.shape[0]/8), math.ceil(cr_downsample.shape[1]/8))

    print("Splitting to 8x8 submatrixes")
    y_split = split_matrix_into_submatrixs(y)
    cb_split = split_matrix_into_submatrixs(cb_downsample)
    cr_split = split_matrix_into_submatrixs(cr_downsample)

    print("paddings")
    y_padding = [matrix if matrix.shape == (
        8, 8) else padding_matrix_to_8_8(matrix) for matrix in y_split]
    cb_padding = [matrix if matrix.shape == (
        8, 8) else padding_matrix_to_8_8(matrix) for matrix in cb_split]
    cr_padding = [matrix if matrix.shape == (
        8, 8) else padding_matrix_to_8_8(matrix) for matrix in cr_split]

    print("DCT")
    y_dct = [dct.DCT(submatrix) for submatrix in y_padding]
    cb_dct = [dct.DCT(submatrix) for submatrix in cb_padding]
    cr_dct = [dct.DCT(submatrix) for submatrix in cr_padding]

    print("Quantization")
    y_quantization = [dct.quantization(submatrix) for submatrix in y_dct]
    cb_quantization = [dct.quantization(submatrix) for submatrix in cb_dct]
    cr_quantization = [dct.quantization(submatrix) for submatrix in cr_dct]

    if entropy:
        print("Compressed entropy: " +
              str(ent.entropy(np.array([y_quantization, cb_quantization, cr_quantization]))))

    print("UnQuantization")
    y_un_quantization = [dct.un_quantization(
        submatrix) for submatrix in y_quantization]
    cb_un_quantization = [dct.un_quantization(
        submatrix) for submatrix in cb_quantization]
    cr_un_quantization = [dct.un_quantization(
        submatrix) for submatrix in cr_quantization]

    print("Invert DCT")
    y_invert_dct = [dct.inverse_DCT(matrix) for matrix in y_un_quantization]
    cb_invert_dct = [dct.inverse_DCT(matrix) for matrix in cb_un_quantization]
    cr_invert_dct = [dct.inverse_DCT(matrix) for matrix in cr_un_quantization]

    print("Concatenate")
    y_big = concatenate_submatrixes_to_big_matrix(y_invert_dct, y_shape)
    cb_big = concatenate_submatrixes_to_big_matrix(cb_invert_dct, cb_shape)
    cr_big = concatenate_submatrixes_to_big_matrix(cr_invert_dct, cr_shape)

    print("Upsample")
    cb_upsample = CbCr_Upsample(cb_big)
    cr_upsample = CbCr_Upsample(cr_big)

    new_image = concatenate_Y_Cb_Cr(y_big, cb_upsample, cr_upsample)

    Image.fromarray(new_image, mode='YCbCr').show()


def main(*argv):    # pragma: no cover
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
    parser.add_argument('-e', action='store_true',
                        help='Show entropy of images')
    parser.add_argument('-d', action='store_true',
                        help='Request input for attach debugger')
    args = parser.parse_args()
    if args.d:
        input("Attach debugger and Enter: ")
    if imghdr.what(args.PATH) != 'bmp':
        print("{} format is not supported for now".format(
            imghdr.what(args.PATH)), file=sys.stderr)
    else:
        compress_image(args.PATH, args.e)

    return 1


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv)

import sys
import math
import dct
import numpy as np
import itertools
import entropy as ent
from typing import List, Tuple
import imagetools


def seperate_to_three_colors(YCrCb_matrix: np.ndarray) -> List[np.ndarray]:
    return [
        YCrCb_matrix[..., 0].copy(), YCrCb_matrix[..., 1].copy(),
        YCrCb_matrix[..., 2].copy()
    ]


def Downsample(matrix: np.ndarray):
    return matrix[::2, ::2]


def Upsample(matrix: np.ndarray) -> np.ndarray:
    return matrix.repeat(2, axis=0).repeat(2, axis=1)


def split_matrix_into_submatrixs(matrix: np.ndarray,
                                 size: int = 8) -> List[np.ndarray]:
    """Split the bitmap to 8*8 matrixs

    Arguments:
        matrix {ndarray} -- The image bitmap

    Returns:
        list -- list of all 8*8 ndarrays matrix
    """
    return [
        np.array([
            [
                matrix[row_index][col_index]
                for col_index in range(col, min(col + size, len(matrix[0])))
            ]  # row in matrix
            for row_index in range(row, min(row + size, len(matrix)))
        ])  # 8*8 matrix
        for row in range(0, len(matrix), size)
        for col in range(0, len(matrix[0]), size)
    ]


# def padding_matrix(matrix: np.ndarray, tosize=8) -> np.ndarray:
#     return np.pad(matrix, ((0, tosize - matrix.shape[0]),
#                            (0, tosize - matrix.shape[1])), 'constant')


def concatenate_submatrixes_to_big_matrix(submatrixes: List[np.ndarray],
                                          shape: Tuple[int]):
    return np.block([
        submatrixes[i:i + shape[1]]
        for i in range(0, len(submatrixes), shape[1])
    ])


def concatenate_three_colors(Y: np.ndarray, Cb: np.ndarray,
                             Cr: np.ndarray) -> np.ndarray:
    return np.dstack((Y, Cb, Cr))


def shape_for_contacting(shape: Tuple) -> Tuple:
    return (math.ceil(shape[0] / 8), math.ceil(shape[1] / 8))

def crop_bitmap(bitmap:np.ndarray, size:int=8)->np.ndarray:
    return bitmap[
            math.floor(bitmap.shape[0]%size/2) : bitmap.shape[0] - math.ceil(bitmap.shape[0]%8/2),
            math.floor(bitmap.shape[1]%size/2) : bitmap.shape[1] - math.ceil(bitmap.shape[1]%size/2),
                ]


def compress_image(path, entropy=False):  # pragma: no cover
    print("Reading file")
    bitmap = imagetools.get_bitmap_from_bmp(path)

    if entropy:
        print("Bitmap entropy: " + str(ent.entropy(bitmap)))
    
    print("Crop image")
    ycrcb_crop = crop_bitmap(bitmap)
    
    print("Converting to YCrCb")
    ycrcb_bitmap = imagetools.BGR_to_YCrCb(ycrcb_crop)

    print("Seperating bitmap to Y, Cb, Cr matrixes")
    y, cb, cr = seperate_to_three_colors(ycrcb_bitmap)

    print("Downsampling")
    cb_downsample = Downsample(cb)
    cr_downsample = Downsample(cr)

    y_shape = (math.ceil(y.shape[0] / 8), math.ceil(y.shape[1] / 8))
    cb_shape = (math.ceil(cb_downsample.shape[0] / 8),
                math.ceil(cb_downsample.shape[1] / 8))
    cr_shape = (math.ceil(cr_downsample.shape[0] / 8),
                math.ceil(cr_downsample.shape[1] / 8))

    print("Splitting to 8x8 submatrixes")
    y_split = split_matrix_into_submatrixs(y)
    cb_split = split_matrix_into_submatrixs(cb_downsample)
    cr_split = split_matrix_into_submatrixs(cr_downsample)

    print("DCT")
    y_dct = [dct.DCT(submatrix) for submatrix in y_split]
    cb_dct = [dct.DCT(submatrix) for submatrix in cb_split]
    cr_dct = [dct.DCT(submatrix) for submatrix in cr_split]

    print("Quantization")
    y_quantization = [dct.quantization(submatrix) for submatrix in y_dct]
    cb_quantization = [dct.quantization(submatrix) for submatrix in cb_dct]
    cr_quantization = [dct.quantization(submatrix) for submatrix in cr_dct]

    if entropy:
        print("Compressed entropy: " + str(
            ent.entropy(
                np.array([y_quantization, cb_quantization, cr_quantization]))))

    print("UnQuantization")
    y_un_quantization = [
        dct.un_quantization(submatrix) for submatrix in y_quantization
    ]
    cb_un_quantization = [
        dct.un_quantization(submatrix) for submatrix in cb_quantization
    ]
    cr_un_quantization = [
        dct.un_quantization(submatrix) for submatrix in cr_quantization
    ]

    print("Invert DCT")
    y_invert_dct = [dct.inverse_DCT(matrix) for matrix in y_un_quantization]
    cb_invert_dct = [dct.inverse_DCT(matrix) for matrix in cb_un_quantization]
    cr_invert_dct = [dct.inverse_DCT(matrix) for matrix in cr_un_quantization]

    print("Concatenate")
    y_big = concatenate_submatrixes_to_big_matrix(y_invert_dct, y_shape)
    cb_big = concatenate_submatrixes_to_big_matrix(cb_invert_dct, cb_shape)
    cr_big = concatenate_submatrixes_to_big_matrix(cr_invert_dct, cr_shape)

    print("Upsample")
    cb_upsample = Upsample(cb_big)
    cr_upsample = Upsample(cr_big)

    new_image = concatenate_three_colors(y_big, cb_upsample, cr_upsample)

    imagetools.show_matrix(new_image, mode='YCrCb')
    imagetools.save_matrix(new_image, mode='YCrCb', dest='img/result.png')

    #Image.fromarray(new_image, mode='YCrCb').show()


def main(*argv):  # pragma: no cover
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
    parser.add_argument(
        '-e', action='store_true', help='Show entropy of images')
    parser.add_argument(
        '-d', action='store_true', help='Request input for attach debugger')
    args = parser.parse_args()
    if args.d:
        input("Attach debugger and Enter: ")
    compress_image(args.PATH, args.e)

    return 1


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv)

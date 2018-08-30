import math
from typing import List, Tuple

import numpy as np

from jpeg import entropy as ent, imagetools, dct


def split_to_three_colors(matrix: np.ndarray) -> List[np.ndarray]:
    return [matrix[..., 0], matrix[..., 1], matrix[..., 2]]


def downsample(matrix: np.ndarray):
    return matrix[::2, ::2]


def upsample(matrix: np.ndarray) -> np.ndarray:
    return matrix.repeat(2, axis=0).repeat(2, axis=1)


def split_matrix_into_sub_matrices(matrix: np.ndarray,
                                   size: int = 8) -> List[np.ndarray]:
    """Split the bitmap to size*size matrices

    Arguments:
        matrix {ndarray} -- The image bitmap

    Returns:
        list -- list of all size*size ndarrays matrix
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


def concatenate_sub_matrices_to_big_matrix(submatrices: List[np.ndarray],
                                           shape: Tuple[int, int]):
    return np.block([
        submatrices[i:i + shape[1]]
        for i in range(0, len(submatrices), shape[1])
    ])


def concatenate_three_colors(y: np.ndarray, cr: np.ndarray,
                             cb: np.ndarray, out: np.ndarray = None) -> np.ndarray:
    return np.stack((y, cr, cb), 2, out)


def shape_for_contacting(shape: Tuple, size=8) -> Tuple:
    return math.ceil(shape[0] / size), math.ceil(shape[1] / size)


def crop_bitmap(bitmap: np.ndarray, size: int = 8) -> np.ndarray:
    return bitmap[math.floor(bitmap.shape[0] % size / 2):bitmap.shape[0] -
                  math.ceil(bitmap.shape[0] % 8 / 2),
                  math.floor(bitmap.shape[1] % size / 2):bitmap.shape[1] -
                  math.ceil(bitmap.shape[1] % size / 2), ]


def compress_image(src_path, dest_path, entropy=False, size=8) -> bool:
    print("Reading file")
    bitmap = imagetools.get_bitmap_from_bmp(src_path)

    if entropy:
        print("Bitmap entropy: " + str(ent.entropy(bitmap)))

    print("Crop image")
    bitmap = crop_bitmap(bitmap)

    print("Converting to YCrCb")
    bitmap = imagetools.bgr_to_ycrcb(bitmap)

    print("Separating bitmap to Y, Cb, Cr matrices")
    y, cb, cr = split_to_three_colors(bitmap)

    print("Downsampling")
    cr = downsample(cr)
    cb = downsample(cb)

    y_shape = shape_for_contacting(y.shape, size)
    cr_shape = shape_for_contacting(cr.shape, size)
    cb_shape = shape_for_contacting(cb.shape, size)

    print("Splitting to {0}x{0} sub-matrices".format(size))
    y = split_matrix_into_sub_matrices(y, size)
    cr = split_matrix_into_sub_matrices(cr, size)
    cb = split_matrix_into_sub_matrices(cb, size)

    print("dct")
    y = [dct.dct(sub_matrix) for sub_matrix in y]
    cr = [dct.dct(sub_matrix) for sub_matrix in cr]
    cb = [dct.dct(sub_matrix) for sub_matrix in cb]

    print("Quantization")
    y = [dct.quantization(submatrix) for submatrix in y]
    cr = [dct.quantization(submatrix) for submatrix in cr]
    cb = [dct.quantization(submatrix) for submatrix in cb]

    if entropy:
        print("Compressed entropy: " + str(
            ent.entropy(
                np.dstack([np.dstack(y), np.dstack(cr), np.dstack(cb)]))))

    print("UnQuantization")
    y = [
        dct.un_quantization(submatrix) for submatrix in y
    ]
    cr = [
        dct.un_quantization(submatrix) for submatrix in cr
    ]
    cb = [
        dct.un_quantization(submatrix) for submatrix in cb
    ]

    print("Invert dct")
    y = [dct.inverse_dct(matrix) for matrix in y]
    cr = [dct.inverse_dct(matrix) for matrix in cr]
    cb = [dct.inverse_dct(matrix) for matrix in cb]

    print("Concatenate")
    y = concatenate_sub_matrices_to_big_matrix(y, y_shape)
    cr = concatenate_sub_matrices_to_big_matrix(cr, cb_shape)
    cb = concatenate_sub_matrices_to_big_matrix(cb, cr_shape)

    print("upsample")
    cr = upsample(cr)
    cb = upsample(cb)

    print("concatenate")
    concatenate_three_colors(y, cr, cb, bitmap)

    # print("ycrcb_to_bgr")
    # bitmap = imagetools.ycrcb_to_bgr(bitmap)

    print("save_matrix")
    imagetools.save_matrix(bitmap, mode='YCrCb', dest=dest_path + '.png')

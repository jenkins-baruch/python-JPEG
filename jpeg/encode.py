import math
from typing import List, Tuple

import numpy as np

from jpeg import entropy as ent, imagetools, dct


def split_to_three_colors(y_cr_cb_matrix: np.ndarray) -> List[np.ndarray]:
    return [
        y_cr_cb_matrix[..., 0].copy(), y_cr_cb_matrix[..., 1].copy(),
        y_cr_cb_matrix[..., 2].copy()
    ]


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
                             cb: np.ndarray) -> np.ndarray:
    return np.dstack((y, cr, cb))


def shape_for_contacting(shape: Tuple, size=8) -> Tuple:
    return math.ceil(shape[0] / size), math.ceil(shape[1] / size)


def crop_bitmap(bitmap: np.ndarray, size: int = 8) -> np.ndarray:
    return bitmap[math.floor(bitmap.shape[0] % size / 2):bitmap.shape[0] -
                  math.ceil(bitmap.shape[0] % 8 / 2),
                  math.floor(bitmap.shape[1] % size / 2):bitmap.shape[1] -
                  math.ceil(bitmap.shape[1] % size / 2), ]


def compress_image(src_path, dest_path, entropy=False,
                   size=8):  # pragma: no cover
    print("Reading file")
    bitmap = imagetools.get_bitmap_from_bmp(src_path)

    if entropy:
        print("Bitmap entropy: " + str(ent.entropy(bitmap)))

    print("Crop image")
    ycrcb_crop = crop_bitmap(bitmap)

    print("Converting to YCrCb")
    ycrcb_bitmap = imagetools.bgr_to_ycrcb(ycrcb_crop)

    print("Separating bitmap to Y, Cb, Cr matrices")
    y, cb, cr = split_to_three_colors(ycrcb_bitmap)

    print("Downsampling")
    cb_downsample = downsample(cb)
    cr_downsample = downsample(cr)

    y_shape = shape_for_contacting(y.shape, size)
    cb_shape = shape_for_contacting(cb_downsample.shape, size)
    cr_shape = shape_for_contacting(cr_downsample.shape, size)

    print("Splitting to 8x8 sub-matrices")
    y_split = split_matrix_into_sub_matrices(y)
    cb_split = split_matrix_into_sub_matrices(cb_downsample)
    cr_split = split_matrix_into_sub_matrices(cr_downsample)

    print("dct")
    y_dct = [dct.dct(sub_matrix) for sub_matrix in y_split]
    cb_dct = [dct.dct(sub_matrix) for sub_matrix in cb_split]
    cr_dct = [dct.dct(sub_matrix) for sub_matrix in cr_split]

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

    print("Invert dct")
    y_invert_dct = [dct.inverse_dct(matrix) for matrix in y_un_quantization]
    cb_invert_dct = [dct.inverse_dct(matrix) for matrix in cb_un_quantization]
    cr_invert_dct = [dct.inverse_dct(matrix) for matrix in cr_un_quantization]

    print("Concatenate")
    y_big = concatenate_sub_matrices_to_big_matrix(y_invert_dct, y_shape)
    cb_big = concatenate_sub_matrices_to_big_matrix(cb_invert_dct, cb_shape)
    cr_big = concatenate_sub_matrices_to_big_matrix(cr_invert_dct, cr_shape)

    print("upsample")
    cb_upsample = upsample(cb_big)
    cr_upsample = upsample(cr_big)

    new_image = concatenate_three_colors(y_big, cb_upsample, cr_upsample)

    imagetools.save_matrix(new_image, mode='YCrCb', dest=dest_path + '.png')

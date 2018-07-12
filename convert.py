import sys
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
    return ((rgb_pixel_to_ycbcr(col[0], col[1], col[2]) for col in row)
            for row in matrix)


def YCbCr_Downstream(matrix):
    """Downstream the Cb and Cr with 4:2:0 correlation

    Arguments:
        matrix {ndarray} -- The image matrix as YCbCr

    Returns:
        ndarray -- The new image matrix with downstreamed YCbCr
    """

    return [[matrix[j-j%2][i-i%2] for i in range(len(matrix[j]))]for j in range(len(matrix))]


# split into Y, Cb, Cr?? where? what is more helpfull?


def split_matrix_into_submatrixs(matrix):
    """Split the bitmap to 8*8 matrixs

    Arguments:
        matrix {ndarray} -- The image bitmap

    Returns:
        list -- list of all 8*8 ndarrays matrix
    """
    
    pass


def centering_values_to_zero(submatrix: np.ndarray) -> np.ndarray:
    """Normalize YCbCr values- remove 128 from each object

    Arguments:
        submatrix {ndarray} -- 8*8 Submatrix

    Returns:
        ndarray -- 8*8 normalized submatrix
    """

    pass


def discerete_cosine_transform(submatrix: np.ndarray) -> np.ndarray:
    """Calculate the DCT that discaide here- https://en.wikipedia.org/wiki/JPEG#Discrete_cosine_transform

    Arguments:
        submatrix {ndarray} -- 8*8 matrix with normalized YCbCr

    Returns:
        ndarray -- DCTed submatrix
    """

    pass


def quantization(submatrix: np.ndarray) -> np.ndarray:
    pass


if __name__ == "__main__":
    get_bitmap_from_bmp(sys.argv[0])

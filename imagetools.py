import numpy as np
from matplotlib import image, pyplot
import cv2
from typing import List

def rgb_pixel_to_ycbcr(bgr: list)->List[np.uint8]:
    return [
        round(0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0]),  # Y'
        round((bgr[2]-round((0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0])))*0.713 + 128),    # Cr
        round((bgr[0]-round((0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0])))*0.564 + 128)    # Cb
    ]


def RGB_to_YCbCr(matrix3D: np.ndarray)->np.ndarray:
    """Converting pixels from RGB (Red, Green, Blue) to YCbCr (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCbCr as 2D array
    """
    return np.apply_along_axis(rgb_pixel_to_ycbcr, 2, matrix3D)


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return image.imread(path)


def save_matrix(matrix: np.ndarray, *, mode: str, dest: str):
    image.imsave(dest, matrix)
    # Image.fromarray(matrix, mode=mode).save(dest)


def show_matrix(matrix: np.ndarray, *, mode: str):
    pyplot.imshow(matrix)
    #Image.fromarray(matrix, mode=mode).show()

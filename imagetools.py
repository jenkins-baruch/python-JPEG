import numpy as np
from cv2 import cv2
from typing import List

def BGR_pixel_to_YCrCb(bgr: list)->List[np.uint8]:
    return [
        round(0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0]),  # Y'
        round((bgr[2]-round((0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0])))*0.713 + 128),    # Cr
        round((bgr[0]-round((0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0])))*0.564 + 128)    # Cb
    ]


def BGR_to_YCrCb(matrix3D: np.ndarray)->np.ndarray:
    """Converting pixels from BGR (Red, Green, Blue) to YCrCb (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCrCb as 2D array
    """
    return np.apply_along_axis(BGR_pixel_to_YCrCb, 2, matrix3D)


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return cv2.imread(path)


def save_matrix(matrix: np.ndarray, *, mode: str, dest: str):
    cv2.imsave(dest, matrix)
    # Image.fromarray(matrix, mode=mode).save(dest)


def show_matrix(matrix: np.ndarray, *, mode: str):
    cv2.imshow(matrix)
    #Image.fromarray(matrix, mode=mode).show()

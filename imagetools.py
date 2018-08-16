import numpy as np
from cv2 import cv2
from typing import List
import random

def BGR_pixel_to_YCrCb(bgr: list)->List[np.uint8]:
    return [
        np.uint8(round(0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0])),  # Y'
        np.uint8(round((bgr[2]-round((0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0])))*0.713 + 128)),    # Cr
        np.uint8(round((bgr[0]-round((0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0])))*0.564 + 128))    # Cb
    ]


def BGR_to_YCrCb(matrix3D: np.ndarray)->np.ndarray:
    """Converting pixels from BGR (Red, Green, Blue) to YCrCb (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCrCb as 2D array
    """
    return np.apply_along_axis(BGR_pixel_to_YCrCb, 2, matrix3D)

def YCrCb_pixel_to_BGR(ycrcb: list)->List[np.uint8]:
    return [
        np.uint8(round(ycrcb[0] + 1.773* (ycrcb[2] - 128))),  # B
        np.uint8(round(ycrcb[0] - 0.714 * (ycrcb[1]-128) - 0.344 * (ycrcb[2]-128))),    # G
        np.uint8(round(ycrcb[0] + 1.403 * (ycrcb[1]-128)))    # R
    ]


def YCrCb_to_BGR(matrix3D: np.ndarray)->np.ndarray:
    return np.apply_along_axis(YCrCb_pixel_to_BGR, 2, matrix3D)


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return cv2.imread(path)


def save_matrix(matrix: np.ndarray, mode:str = 'BGR', dest: str = 'tmp.png'):
    if mode == 'YCrCb':
        matrix = YCrCb_to_BGR(matrix)
        mode = 'BGR'
    if mode != 'BGR':
        raise Exception('{} currently not supported to save.'.format(mode))
    cv2.imwrite(dest, matrix)


def show_matrix(matrix: np.ndarray, mode='BGR', name='tmp'):
    if mode == 'YCrCb':
        matrix = YCrCb_to_BGR(matrix)
        mode = 'BGR'
    if mode != 'BGR':
        raise Exception('{} currently not supported to show.'.format(mode))
    cv2.imshow(name, matrix)
    cv2.waitKey(20)
    print("Enter to close image: ")
    cv2.destroyAllWindows()

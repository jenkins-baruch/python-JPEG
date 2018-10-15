import numpy as np
from cv2 import cv2
from typing import List


def __y_calculate(bgr: list) -> float:
    return 0.299 * bgr[2] + 0.587 * bgr[1] + 0.114 * bgr[0]


def bgr_pixel_to_ycrcb(bgr: list) -> List[int]:
    return [
        round(__y_calculate(bgr)),  # Y'
        round((bgr[2] - round(__y_calculate(bgr))) * 0.713 + 128),  # Cr
        round((bgr[0] - round(__y_calculate(bgr))) * 0.564 + 128)  # Cb
    ]


def bgr_to_ycrcb(matrix3d: np.ndarray) -> np.ndarray:
    """Converting pixels from BGR (Red, Green, Blue) to YCrCb (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCrCb as 2D array
    """
    return np.apply_along_axis(bgr_pixel_to_ycrcb, 2, matrix3d)


def ycrcb_pixel_to_bgr(ycrcb: list) -> List[np.uint8]:
    return [
        np.uint8(np.clip(round(ycrcb[0] + 1.773 * (ycrcb[2] - 128)), 0, 255)),  # B
        np.uint8(np.clip(round(ycrcb[0] - 0.714 * (ycrcb[1] - 128) - 0.344 * (ycrcb[2] - 128)), 0, 255)),  # G
        np.uint8(np.clip(round(ycrcb[0] + 1.403 * (ycrcb[1] - 128)), 0, 255))  # R
    ]


def ycrcb_to_bgr(matrix3d: np.ndarray) -> np.ndarray:
    return np.apply_along_axis(ycrcb_pixel_to_bgr, 2, matrix3d)


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return cv2.imread(path)


def save_matrix(matrix: np.ndarray, mode: str = 'RGB', dest: str = 'tmp.png'):
    if mode == 'YCrCb':
        matrix = ycrcb_to_bgr(matrix)
    cv2.imwrite(dest, matrix)


def show_matrix(matrix: np.ndarray, mode='BGR', name='tmp'):
    if mode == 'YCrCb':
        matrix = ycrcb_to_bgr(matrix)
        mode = 'BGR'
    if mode != 'BGR':
        raise Exception('{} currently not supported to show.'.format(mode))
    cv2.imshow(name, matrix)
    cv2.waitKey(20)
    input("Enter to close image: ")
    cv2.destroyAllWindows()

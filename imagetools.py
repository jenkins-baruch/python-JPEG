import numpy as np
from matplotlib import image, pyplot
import cv2


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return image.imread(path)


def save_matrix(matrix: np.ndarray, *, mode: str, dest: str):
    image.imsave(dest, matrix)
    # Image.fromarray(matrix, mode=mode).save(dest)


def show_matrix(matrix: np.ndarray, *, mode: str):
    pyplot.imshow(matrix)
    #Image.fromarray(matrix, mode=mode).show()

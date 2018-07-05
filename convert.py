import sys
import numpy as np
from PIL import Image


def get_bitmap_from_bmp(path: str) -> np.ndarray:
    """Method to read .bmp file and return the image bitmap

    Arguments:
        path {str} -- The .bmp file path

    Returns:
        np.ndarray -- 2D array that present the bitmap
    """

    # HowTo:
    # Search "python read image matrix with PIL"
    # Search "python PIL image to numpy array"

    pass


if __name__ == "__main__":
    get_bitmap_from_bmp(sys.argv[0])

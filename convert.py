import sys
from numpy import ndarray
from PIL import Image


def get_bitmap_from_bmp(path: str) -> ndarray:
    """Method to read .bmp file and return the image bitmap

    Arguments:
        path {str} -- The .bmp file path

    Returns:
        np.ndarray -- 2D array that present the bitmap,
        each pixel is array of [R,G,B]
    """

    # HowTo:
    # Search "python read image matrix with PIL"
    # Search "python PIL image to numpy array"

    pass


def RGB_to_YCbCr(matrix: ndarray)->ndarray:
    """Converting pixels from RGB (Red, Green, Blue) to YCbCr (luma, blue-difference, red-difference)

    Arguments:
        matrix {ndarray} -- The image Bitmap as 2D array

    Returns:
        ndarray -- The new Bitmap with YCbCr as 2D array
    """

    pass

def YCbCr_Downstream(matrix:ndarray)->ndarray:
    """Downstream the Cb and Cr with 4:2:0 correlation
    
    Arguments:
        matrix {ndarray} -- The image matrix as YCbCr
    
    Returns:
        ndarray -- The new image matrix with downstreamed YCbCr
    """

    pass

if __name__ == "__main__":
    get_bitmap_from_bmp(sys.argv[0])

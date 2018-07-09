import sys
from numpy import ndarray
from PIL import Image
import matplotlib


get_bitmap_from_bmp = lambda path: matplotlib.image.imread(path)



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

# split into Y, Cb, Cr?? where? what is more helpfull?

def split_matrix_into_submatrixs(matrix:ndarray)->list:
    """Split the bitmap to 8*8 matrixs
    
    Arguments:
        matrix {ndarray} -- The image bitmap
    
    Returns:
        list -- list of all 8*8 ndarrays matrix
    """

    pass

def centering_values_to_zero(submatrix:ndarray)->ndarray:
    """Normalize YCbCr values- remove 128 from each object
    
    Arguments:
        submatrix {ndarray} -- 8*8 Submatrix
    
    Returns:
        ndarray -- 8*8 normalized submatrix
    """

    pass

def discerete_cosine_transform(submatrix: ndarray)->ndarray:
    """Calculate the DCT that discaide here- https://en.wikipedia.org/wiki/JPEG#Discrete_cosine_transform
    
    Arguments:
        submatrix {ndarray} -- 8*8 matrix with normalized YCbCr
    
    Returns:
        ndarray -- DCTed submatrix
    """

    pass

def quantization(submatrix: ndarray)->ndarray:
    pass

if __name__ == "__main__":
    get_bitmap_from_bmp(sys.argv[0])

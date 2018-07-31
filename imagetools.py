import numpy as np
from PIL import Image
from matplotlib import image, pyplot

def get_bitmap_from_bmp(path: str) -> np.ndarray:
    return image.imread(path)

def save_image(matrix: np.ndarray,*, mode:str, dest:str):
    Image()
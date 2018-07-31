import sys
import encode
import imagetools

path = sys.argv[1]
img_matrix = imagetools.get_bitmap_from_bmp(path)
imagetools.save_matrix(img_matrix, mode='RGB', dest='img/rgb.bmp')


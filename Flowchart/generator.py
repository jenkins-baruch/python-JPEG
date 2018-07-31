import sys
import os
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root_dir)
os.chdir(root_dir)
import imagetools
import encode

path = sys.argv[1]
img_matrix = imagetools.get_bitmap_from_bmp(path)
#imagetools.save_matrix(img_matrix, mode='RGB', dest='img/rgb.bmp')
ycbcr = encode.RGB_to_YCbCr(img_matrix)
imagetools.save_matrix(ycbcr, mode="YCbCr", dest="")

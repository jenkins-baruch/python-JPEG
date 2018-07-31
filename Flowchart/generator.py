import sys
import os
print(os.path.abspath(os.curdir))
os.chdir("..")
sys.path.insert(0, os.path.abspath(os.curdir))
import imagetools
import encode

path = sys.argv[1]
img_matrix = imagetools.get_bitmap_from_bmp(path)
#imagetools.save_matrix(img_matrix, mode='RGB', dest='img/rgb.bmp')
ycbcr = encode.RGB_to_YCbCr(img_matrix)
imagetools.save_matrix(ycbcr, mode="YCbCr",dest="")


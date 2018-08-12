import sys
import os
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root_dir)
os.chdir(root_dir)
import imagetools
import encode
import cv2

path = sys.argv[1]
img_matrix = imagetools.get_bitmap_from_bmp(path)

ycbcr = encode.RGB_to_YCbCr(img_matrix)
imagetools.show_matrix(ycbcr, mode='YCbCr')
imagetools.save_matrix(ycbcr, mode="YCbCr",
                       dest="Flowchart/results/ycbcr.jpeg")
jpg = imagetools.get_bitmap_from_bmp("Flowchart/results/ycbcr.jpeg")
input()
imagetools.show_matrix(jpg, mode='YCbCr')

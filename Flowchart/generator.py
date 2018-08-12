import sys
import os
import cv2

# import from project folder
root_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, root_dir)
os.chdir(root_dir)
import imagetools
import encode


path = sys.argv[1]

img_matrix = imagetools.get_bitmap_from_bmp(path)

ycrcb = imagetools.BGR_to_YCrCb(img_matrix)
imagetools.show_matrix(ycrcb, mode='')
imagetools.save_matrix(ycrcb, mode="",
                       dest="Flowchart/results/ycrcb.jpeg")
jpg = imagetools.get_bitmap_from_bmp("Flowchart/results/ycrcb.jpeg")
input()
imagetools.show_matrix(jpg, mode='')

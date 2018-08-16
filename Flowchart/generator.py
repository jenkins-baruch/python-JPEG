import sys
import os
from cv2 import cv2
import numpy as np

# import from project folder
dirname = os.path.dirname(__file__)
root_dir = os.path.dirname(dirname)
sys.path.insert(0, root_dir)
os.chdir(root_dir)
import imagetools
import encode

# Read image
path = "img/moto.png"# sys.argv[1]
print("Read image " + path)
img = imagetools.get_bitmap_from_bmp(path)

# Convert to YCrCb
print("Convert to YCrCb")
img_ycrcb = imagetools.BGR_to_YCrCb(img)

print("Seperate colors")
img_ycbcr_y, img_ycbcr_cr, img_ycbcr_cb = encode.seperate_to_three_colors(img_ycrcb)
img_b, img_g, img_r = encode.seperate_to_three_colors(img)

print("Const matrixes")
ycrcb_channel_const = np.ones_like(img_ycbcr_y) * 127.5
gbr_channel_const = np.zeros_like(img_b)

print("Generate YCrCb colors images")
img_ycbcr_y = encode.concatenate_three_colors(img_ycbcr_y, ycrcb_channel_const, ycrcb_channel_const)
img_ycbcr_cr = encode.concatenate_three_colors(ycrcb_channel_const, img_ycbcr_cr, ycrcb_channel_const)
img_ycbcr_cb = encode.concatenate_three_colors(ycrcb_channel_const, ycrcb_channel_const, img_ycbcr_cb)

imagetools.save_matrix(img_ycbcr_y, mode='YCrCb', dest=os.path.join(dirname, 'channel_y.png'))
imagetools.save_matrix(img_ycbcr_cr, mode='YCrCb', dest=os.path.join(dirname, 'channel_cr.png'))
imagetools.save_matrix(img_ycbcr_cb, mode='YCrCb', dest=os.path.join(dirname, 'channel_cb.png'))

print("Generate BGR colors images")
img_b = encode.concatenate_three_colors(img_b, gbr_channel_const, gbr_channel_const)
img_g = encode.concatenate_three_colors(gbr_channel_const, img_g, gbr_channel_const)
img_r = encode.concatenate_three_colors(gbr_channel_const, gbr_channel_const, img_r)

imagetools.save_matrix(img_b, dest=os.path.join(dirname, 'channel_b.png'))
imagetools.save_matrix(img_g, dest=os.path.join(dirname, 'channel_g.png'))
imagetools.save_matrix(img_r,dest=os.path.join(dirname, 'channel_r.png'))

input("END")
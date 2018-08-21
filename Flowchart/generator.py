import sys
import os
from cv2 import cv2
import numpy as np
import math

# import from project folder
dirname = os.path.dirname(__file__)
root_dir = os.path.dirname(dirname)
sys.path.insert(0, root_dir)
os.chdir(root_dir)
import imagetools
import encode
import dct

# Read image
path = "img/moto.png"  # sys.argv[1]
print("Read image " + path)
img = imagetools.get_bitmap_from_bmp(path)
imagetools.save_matrix(img, dest=os.path.join(dirname, 'original.png'))

# Convert to YCrCb
print("Convert to YCrCb")
img_ycrcb = imagetools.BGR_to_YCrCb(img)

print("Seperate colors")
img_channel_y, img_channel_cr, img_channel_cb = encode.seperate_to_three_colors(
    img_ycrcb)
img_channel_b, img_channel_g, img_channel_r = encode.seperate_to_three_colors(
    img)

print("Const matrixes")
ycrcb_channel_const = np.ones_like(img_channel_y) * 127.5
gbr_channel_const = np.zeros_like(img_channel_b)

print("Generate YCrCb colors images")
img_matrix_y = encode.concatenate_three_colors(
    img_channel_y, ycrcb_channel_const, ycrcb_channel_const)
img_matrix_cr = encode.concatenate_three_colors(
    ycrcb_channel_const, img_channel_cr, ycrcb_channel_const)
img_matrix_cb = encode.concatenate_three_colors(
    ycrcb_channel_const, ycrcb_channel_const, img_channel_cb)

imagetools.save_matrix(
    img_matrix_y, mode='YCrCb', dest=os.path.join(dirname, 'channel_y.png'))
imagetools.save_matrix(
    img_matrix_cr, mode='YCrCb', dest=os.path.join(dirname, 'channel_cr.png'))
imagetools.save_matrix(
    img_matrix_cb, mode='YCrCb', dest=os.path.join(dirname, 'channel_cb.png'))

print("Generate BGR colors images")
img_matrix_b = encode.concatenate_three_colors(
    img_channel_b, gbr_channel_const, gbr_channel_const)
img_matrix_g = encode.concatenate_three_colors(
    gbr_channel_const, img_channel_g, gbr_channel_const)
img_matrix_r = encode.concatenate_three_colors(
    gbr_channel_const, gbr_channel_const, img_channel_r)

imagetools.save_matrix(
    img_matrix_b, dest=os.path.join(dirname, 'channel_b.png'))
imagetools.save_matrix(
    img_matrix_g, dest=os.path.join(dirname, 'channel_g.png'))
imagetools.save_matrix(
    img_matrix_r, dest=os.path.join(dirname, 'channel_r.png'))

print("Downsapling")
img_channel_cb_downsampled = encode.Upsample(encode.Downsample(img_channel_cb))
img_channel_cr_downsampled = encode.Upsample(encode.Downsample(img_channel_cr))

img_channel_g_downsampled = encode.Upsample(encode.Downsample(img_channel_g))
img_channel_r_downsampled = encode.Upsample(encode.Downsample(img_channel_r))

imagetools.save_matrix(
    encode.concatenate_three_colors(img_channel_y, img_channel_cr_downsampled,
                                    img_channel_cb_downsampled),
    mode='YCrCb',
    dest=os.path.join(dirname, 'ycrcb_downsapling.png'))
imagetools.save_matrix(
    encode.concatenate_three_colors(img_channel_b, img_channel_g_downsampled,
                                    img_channel_r_downsampled),
    dest=os.path.join(dirname, 'bgr_downsapling.png'))


def local_dct(y, cr, cb, dst, size=8):
    y_shape = (math.ceil(y.shape[0] / 8), math.ceil(y.shape[1] / 8))
    cb_shape = (math.ceil(cr.shape[0] / 8), math.ceil(cr.shape[1] / 8))
    cr_shape = (math.ceil(cb.shape[0] / 8), math.ceil(cb.shape[1] / 8))
    print("Split and padding to submatrixes")
    img_channel_y_split = [
        encode.padding_matrix(matrix, size)
        for matrix in encode.split_matrix_into_submatrixs(y, size)
    ]
    img_channel_cr_split = [
        encode.padding_matrix(matrix, size)
        for matrix in encode.split_matrix_into_submatrixs(cr, size)
    ]
    img_channel_cb_split = [
        encode.padding_matrix(matrix, size)
        for matrix in encode.split_matrix_into_submatrixs(cb, size)
    ]

    print("DCT and Quantization submatrixes")
    img_channel_y_split = [
        dct.quantization(dct.DCT(submatrix))
        for submatrix in img_channel_y_split
    ]
    img_channel_cr_split = [
        dct.quantization(dct.DCT(submatrix))
        for submatrix in img_channel_cr_split
    ]
    img_channel_cb_split = [
        dct.quantization(dct.DCT(submatrix))
        for submatrix in img_channel_cb_split
    ]

    print("Invert DCT and UnQuantization")
    img_channel_y_split = [
        dct.inverse_DCT(dct.un_quantization(submatrix))
        for submatrix in img_channel_y_split
    ]
    img_channel_cr_split = [
        dct.inverse_DCT(dct.un_quantization(submatrix))
        for submatrix in img_channel_cr_split
    ]
    img_channel_cb_split = [
        dct.inverse_DCT(dct.un_quantization(submatrix))
        for submatrix in img_channel_cb_split
    ]

    print("Concatenate")
    y_big = encode.concatenate_submatrixes_to_big_matrix(
        img_channel_y_split, y_shape)
    cb_big = encode.concatenate_submatrixes_to_big_matrix(
        img_channel_cr_split, cb_shape)
    cr_big = encode.concatenate_submatrixes_to_big_matrix(
        img_channel_cb_split, cr_shape)

    imagetools.save_matrix(
        encode.concatenate_three_colors(y_big, cb_big, cr_big),
        mode='YCrCb',
        dest=os.path.join(dirname, dst + '.png'))


# local_dct(img_channel_y, img_channel_cr, img_channel_cb, "ycrcb_split8_dct")

local_dct(img_channel_y, img_channel_cr, img_channel_cb, "ycrcb_split32_dct",
          32)

input("END")

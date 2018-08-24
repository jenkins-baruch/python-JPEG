import os
import sys

import numpy as np

from jpeg import imagetools, encode, dct

if __name__ == '__main__':
    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    root_dir = os.path.dirname(src_dir)

    # Read image
    path = sys.argv[1]
    print("Read image " + path)
    img = encode.crop_bitmap(imagetools.get_bitmap_from_bmp(path))
    imagetools.save_matrix(img, dest=os.path.join(src_dir, 'original.png'))

    # Convert to YCrCb
    print("Convert to YCrCb")
    img_ycrcb = imagetools.bgr_to_ycrcb(img)

    print("Seperate colors")
    img_channel_y, img_channel_cr, img_channel_cb = encode.split_to_three_colors(
        img_ycrcb)
    img_channel_b, img_channel_g, img_channel_r = encode.split_to_three_colors(
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
        img_matrix_y, mode='YCrCb', dest=os.path.join(src_dir, 'channel_y.png'))
    imagetools.save_matrix(
        img_matrix_cr, mode='YCrCb', dest=os.path.join(src_dir, 'channel_cr.png'))
    imagetools.save_matrix(
        img_matrix_cb, mode='YCrCb', dest=os.path.join(src_dir, 'channel_cb.png'))

    print("Generate BGR colors images")
    img_matrix_b = encode.concatenate_three_colors(
        img_channel_b, gbr_channel_const, gbr_channel_const)
    img_matrix_g = encode.concatenate_three_colors(
        gbr_channel_const, img_channel_g, gbr_channel_const)
    img_matrix_r = encode.concatenate_three_colors(
        gbr_channel_const, gbr_channel_const, img_channel_r)

    imagetools.save_matrix(
        img_matrix_b, dest=os.path.join(src_dir, 'channel_b.png'))
    imagetools.save_matrix(
        img_matrix_g, dest=os.path.join(src_dir, 'channel_g.png'))
    imagetools.save_matrix(
        img_matrix_r, dest=os.path.join(src_dir, 'channel_r.png'))

    print("Downsapling")
    img_channel_cb_downsampled = encode.upsample(encode.downsample(img_channel_cb))
    img_channel_cr_downsampled = encode.upsample(encode.downsample(img_channel_cr))

    img_channel_g_downsampled = encode.upsample(encode.downsample(img_channel_g))
    img_channel_r_downsampled = encode.upsample(encode.downsample(img_channel_r))

    imagetools.save_matrix(
        encode.concatenate_three_colors(img_channel_y, img_channel_cr_downsampled, img_channel_cb_downsampled),
        mode='YCrCb',
        dest=os.path.join(src_dir, 'ycrcb_downsapling.png'))
    imagetools.save_matrix(
        encode.concatenate_three_colors(img_channel_b, img_channel_g_downsampled,
                                        img_channel_r_downsampled),
        dest=os.path.join(src_dir, 'bgr_downsapling.png'))


    def local_dct(y, cr, cb, dst, size=8):
        y_shape = encode.shape_for_contacting(y.shape, size)
        cb_shape = encode.shape_for_contacting(cb.shape, size)
        cr_shape = encode.shape_for_contacting(cr.shape, size)
        print("Split and padding to submatrices")
        img_channel_y_split = [matrix for matrix in encode.split_matrix_into_sub_matrices(y, size)]
        img_channel_cr_split = [matrix for matrix in encode.split_matrix_into_sub_matrices(cr, size)]
        img_channel_cb_split = [matrix for matrix in encode.split_matrix_into_sub_matrices(cb, size)]

        print("DCT submatrices")
        img_channel_y_split = [
            dct.DCT(submatrix)
            for submatrix in img_channel_y_split
        ]
        img_channel_cr_split = [
            dct.DCT(submatrix)
            for submatrix in img_channel_cr_split
        ]
        img_channel_cb_split = [
            dct.DCT(submatrix)
            for submatrix in img_channel_cb_split
        ]

        if size == 8:
            print("Quantization submatrices")
            img_channel_y_split = [
                dct.quantization(submatrix)
                for submatrix in img_channel_y_split
            ]
            img_channel_cr_split = [
                dct.quantization(submatrix)
                for submatrix in img_channel_cr_split
            ]
            img_channel_cb_split = [
                dct.quantization(submatrix)
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
        y_big = encode.concatenate_sub_matrices_to_big_matrix(
            img_channel_y_split, y_shape)
        cb_big = encode.concatenate_sub_matrices_to_big_matrix(
            img_channel_cr_split, cb_shape)
        cr_big = encode.concatenate_sub_matrices_to_big_matrix(
            img_channel_cb_split, cr_shape)

        imagetools.save_matrix(
            encode.concatenate_three_colors(y_big, cb_big, cr_big),
            mode='YCrCb',
            dest=os.path.join(src_dir, dst + '.png'))


    local_dct(img_channel_y, img_channel_cr, img_channel_cb, "ycrcb_split8_dct")
    local_dct(img_channel_y, img_channel_cr, img_channel_cb, "ycrcb_split16_dct", 16)
    local_dct(img_channel_y, img_channel_cr, img_channel_cb, "ycrcb_split32_dct", 32)

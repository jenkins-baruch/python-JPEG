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
    imagetools.save_matrix(
        img, dest=os.path.join(src_dir, 'original_crop.png'))

    def split_and_downsample(matrix, mode):
        print("Split {} colors".format(mode))
        img_channel_a, img_channel_b, img_channel_c = encode.split_to_three_colors(
            matrix)

        channel_const = np.zeros_like(img_channel_a)
        if mode == 'YCrCb':
            channel_const = channel_const + 127.5

        print("Generate {} colors images".format(mode))

        imagetools.save_matrix(
            encode.concatenate_three_colors(img_channel_a, channel_const,
                                            channel_const),
            mode=mode,
            dest=os.path.join(src_dir, mode + '_channel_a.png'))

        imagetools.save_matrix(
            encode.concatenate_three_colors(channel_const, img_channel_b,
                                            channel_const),
            mode=mode,
            dest=os.path.join(src_dir, mode + '_channel_b.png'))

        imagetools.save_matrix(
            encode.concatenate_three_colors(channel_const, channel_const,
                                            img_channel_c),
            mode=mode,
            dest=os.path.join(src_dir, mode + '_channel_c.png'))

        print('Downsampling ' + mode)
        img_channel_b = encode.upsample(encode.downsample(img_channel_b))
        img_channel_c = encode.upsample(encode.downsample(img_channel_c))

        imagetools.save_matrix(
            encode.concatenate_three_colors(img_channel_a, img_channel_b,
                                            img_channel_c),
            mode=mode,
            dest=os.path.join(src_dir, mode + '_downsapling.png'))

    split_and_downsample(img, 'BGR')
    print("bgr_to_ycrcb")
    img = imagetools.bgr_to_ycrcb(img)
    split_and_downsample(img, 'YCrCb')

    def local_dct(matrix, dst, size=8):
        y, cr, cb = encode.split_to_three_colors(matrix)

        y_shape = encode.shape_for_contacting(y.shape, size)
        cb_shape = encode.shape_for_contacting(cb.shape, size)
        cr_shape = encode.shape_for_contacting(cr.shape, size)

        print("Split and padding to submatrices")
        y = [
            matrix
            for matrix in encode.split_matrix_into_sub_matrices(y, size)
        ]
        cr = [
            matrix
            for matrix in encode.split_matrix_into_sub_matrices(cr, size)
        ]
        cb = [
            matrix
            for matrix in encode.split_matrix_into_sub_matrices(cb, size)
        ]

        print("dct submatrices")
        y = [dct.dct(submatrix) for submatrix in y]
        cr = [dct.dct(submatrix) for submatrix in cr]
        cb = [dct.dct(submatrix) for submatrix in cb]

        print("Quantization submatrices")
        y = [dct.quantization(submatrix) for submatrix in y]
        cr = [dct.quantization(submatrix) for submatrix in cr]
        cb = [dct.quantization(submatrix) for submatrix in cb]

        print("Invert dct and UnQuantization")
        y = [
            dct.inverse_dct(dct.un_quantization(submatrix)) for submatrix in y
        ]
        cr = [
            dct.inverse_dct(dct.un_quantization(submatrix)) for submatrix in cr
        ]
        cb = [
            dct.inverse_dct(dct.un_quantization(submatrix)) for submatrix in cb
        ]

        print("Concatenate")
        y = encode.concatenate_sub_matrices_to_big_matrix(y, y_shape)
        cr = encode.concatenate_sub_matrices_to_big_matrix(cr, cr_shape)
        cb = encode.concatenate_sub_matrices_to_big_matrix(cb, cb_shape)

        print("Save")
        imagetools.save_matrix(
            encode.concatenate_three_colors(y, cr, cb, matrix),
            mode='YCrCb',
            dest=os.path.join(src_dir, dst + '.png'))

    print("dct8")
    local_dct(img, "ycrcb_split8_dct")
    print("dct16")
    local_dct(img, "ycrcb_split16_dct", 16)
    print("dct32")
    local_dct(img, "ycrcb_split32_dct", 32)

import unittest

from cv2 import cv2

from jpeg import imagetools
from test import *


class CaseGetBitmapFromBmp(unittest.TestCase):
    @staticmethod
    def test_whiteImage_getAllWhite():
        test_matrix = generate_one_color_matrix(8 ** 3, 8 ** 3, [255, 255, 255])
        np.testing.assert_array_equal(
            imagetools.get_bitmap_from_bmp(os.path.join(src, "white.bmp")),
            test_matrix)

    @staticmethod
    def test_BlackImage_getAllBlack():
        test_matrix = generate_one_color_matrix(8 ** 3, 8 ** 3, [0, 0, 0])
        np.testing.assert_array_equal(
            imagetools.get_bitmap_from_bmp(os.path.join(src, "black.bmp")),
            test_matrix)

    @staticmethod
    def test_ColoredImage_getAllColored():
        test_matrix = get_colored_matrix(255, 255)
        np.testing.assert_array_equal(
            imagetools.get_bitmap_from_bmp(os.path.join(src, "colored.bmp")),
            test_matrix)

    @staticmethod
    def test_NotProd8Size_ColoredImage():
        test_matrix = get_colored_matrix(100, 100)
        np.testing.assert_array_equal(
            imagetools.get_bitmap_from_bmp(
                os.path.join(src, "colored_100x100.bmp")), test_matrix)


class CaseBGRPixelToYCrCb(unittest.TestCase):
    def test_white_pixel(self):
        original = [255, 255, 255]
        expected = [255, 128, 128]
        actual = imagetools.bgr_pixel_to_ycrcb(original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_black_pixel(self):
        original = [0, 0, 0]
        expected = [0, 128, 128]
        actual = imagetools.bgr_pixel_to_ycrcb(original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_color_pixel(self):
        original = [48, 113, 219]  # #3071db Tchelet
        expected = [137, 186, 78]
        actual = imagetools.bgr_pixel_to_ycrcb(original)
        self.assertSequenceEqual(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))


class CaseBGRToYCrCb(unittest.TestCase):
    @staticmethod
    def test_matrix():
        original = np.array([
            [(255, 255, 255), (48, 113, 219), (0, 0, 0)],
            [(0, 0, 0), (48, 113, 219), (255, 255, 255)],
            [(48, 113, 219), (0, 0, 0), (0, 0, 0)],
            [(255, 255, 255), (48, 113, 219), (255, 255, 255)]
        ])
        expected = np.array([
            [(255, 128, 128), (137, 186, 78), (0, 128, 128)],
            [(0, 128, 128), (137, 186, 78), (255, 128, 128)],
            [(137, 186, 78), (0, 128, 128), (0, 128, 128)],
            [(255, 128, 128), (137, 186, 78), (255, 128, 128)]
        ])
        actual = imagetools.bgr_to_ycrcb(original)
        np.testing.assert_array_equal(
            expected, actual,
            "The original pixel- {} converted to {} and not to {} that expected"
            .format(original, actual, expected))

    def test_vs_cv2(self):
        im = cv2.imread(os.path.join(src, "colored.bmp"))
        expected = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)
        actual = imagetools.bgr_to_ycrcb(im)
        different = np.count_nonzero(actual - expected) / np.prod(im.shape)
        self.assertLessEqual(different, 1 / 100)


class CaseYCrCbToBGR(unittest.TestCase):
    def test_matrix(self):
        original = np.array([
            [(255, 128, 128), (137, 186, 78), (0, 128, 128)],
            [(0, 128, 128), (137, 186, 78), (255, 128, 128)],
            [(137, 186, 78), (0, 128, 128), (0, 128, 128)],
            [(255, 128, 128), (137, 186, 78), (255, 128, 128)]
        ])
        expected = np.array([
            [(255, 255, 255), (48, 113, 219), (0, 0, 0)],
            [(0, 0, 0), (48, 113, 219), (255, 255, 255)],
            [(48, 113, 219), (0, 0, 0), (0, 0, 0)],
            [(255, 255, 255), (48, 113, 219), (255, 255, 255)]
        ])
        actual = imagetools.ycrcb_to_bgr(original)
        max_different = np.max(np.abs(expected - actual))
        self.assertLessEqual(max_different, 1,
                             "There is different in size {} between expected and actual\nexpected:\n{}\nactual:\n{}"
                             .format(max_different, expected, actual))

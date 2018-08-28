import unittest
from cv2 import cv2
import numpy as np
from jpeg import encode
import shutil
import os

dirname = os.path.dirname(__file__)
original_path = os.path.join(dirname, '..', 'src', 'original.png')
test_path = os.path.join(dirname, 'test.png')
result_path = os.path.join(dirname, 'result.png')


class CaseIntegrationTests(unittest.TestCase):
    @classmethod
    def setUp(cls):
        shutil.copyfile(original_path, test_path)

    def test_basic(self):
        self.run_compress()

    def test_entropy(self):
        self.run_compress(True)

    def test_16(self):
        self.run_compress(size=16)

    def test_32(self):
        self.run_compress(size=32)

    def run_compress(self, entropy=False, size=8):
        self.assertTrue(
            encode.compress_image(test_path, result_path, entropy, size),
            "The method not return or return False")
        self.assertTrue(
            os.path.isfile(result_path), "The result.png not exist")
        self.assertGreater(
            os.path.getsize(result_path), 0, "The file is 0 size")

    @classmethod
    def tearDown(cls):
        os.remove(test_path)
        os.remove(result_path)


class CaseConcatenateColors(unittest.TestCase):
    @classmethod
    def setUp(cls):
        shutil.copyfile(original_path, test_path)

    def test_concatenate_colors(self):
        img = cv2.imread(test_path)
        b, g, r = cv2.split(img)
        result = encode.concatenate_three_colors(b, g, r)
        np.testing.assert_array_equal(img, result, "Concatenating fail")

    @classmethod
    def tearDown(cls):
        os.remove(test_path)

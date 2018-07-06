import unittest


class ConvertingTest(unittest.TestCase):
    @unittest.expectedFailure
    def test_convertBitmap_getMatrix(self):
        self.assertEqual(1, 2)

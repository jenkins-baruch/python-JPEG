import unittest
import entropy
import numpy as np

class case_entropy(unittest.TestCase):
    def test_entropy(self):
        words = [
            "love","love","love","love",
            "wave","wave","wave","wave"
        ]
        original = np.array([list(word) for word in words])
        expected = 2.5
        actual = entropy.entropy(original)
        self.assertAlmostEqual(expected, actual)
    
    def test_entropy_2(self):
        original =np.array([
            [12,15,22,8,4,4,4,4,4,4,4,4,4,4,4,4],
            [23,6,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
        ])
        expected = 1.18
        actual = entropy.entropy(original)
        self.assertAlmostEqual(expected, actual, places=2)

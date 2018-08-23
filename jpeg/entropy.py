import numpy as np
import math


def __get_frequencies(matrix: np.ndarray, elements_count: int) -> list:
    return [c / elements_count for c in np.unique(matrix, return_counts=True)[1]]


def __get_entropy(freqs: list) -> float:
    return -sum(p * math.log2(p) for p in freqs)


def entropy(matrix: np.ndarray) -> float:
    return __get_entropy(__get_frequencies(matrix, np.prod(matrix.shape)))

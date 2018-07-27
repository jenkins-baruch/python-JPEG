import collections
import numpy as np
import math


def __get_frequencies(matrix2D : np.ndarray)->list:
    return [c /(matrix2D.shape[0]*matrix2D.shape[1]) for c in np.unique(matrix2D, return_counts=True)[1]]

def __get_entropy(freqs:list)->float:
    return -sum(p*math.log2(p) for p in freqs)

def entropy(matrix2D:np.ndarray)->float:
    return __get_entropy(__get_frequencies(matrix2D))

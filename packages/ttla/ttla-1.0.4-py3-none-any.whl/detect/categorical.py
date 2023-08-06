from collections import Counter
import math


def is_categorical(col):
    """
    if the given column is categorical or not
    :param col: pandas series
    :return: true of false
    """
    cc = Counter(col)
    if len(cc.keys()) <= math.sqrt(len(col)):
        return True
    return False






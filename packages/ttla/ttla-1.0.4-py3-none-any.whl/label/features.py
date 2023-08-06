import commons
import math
import numpy as np
from collections import Counter


def transform_if_needed(kind, nums):
    """
    Transform the data if we need depending on the kind
    :param kind:
    :param nums:
    :return:
    """
    new_nums = []
    if kind in [commons.COUNTS]:
        for n in nums:
            new_nums.append(math.sqrt(n))
    else:
        new_nums = nums

    return new_nums


def compute_features(kind, nums):
    """
    :param kind:
    :param nums:
    :return:
    """
    transformed = transform_if_needed(kind=kind, nums=nums)
    if kind in [commons.HIERARCHICAL]:
        return None
    features = [trimean_feature(transformed)]
    if kind == commons.CATEGORICAL:
        features += categorical_ratio_feature(transformed)
    else:
        # print("debugging")
        # print("features: "+str(features))
        # print("transformed: "+str(transformed))
        features += [tstd_feature(trimean=features[0], nums=transformed)]
        # print("success: "+str(features))
    return features


def trimean_feature(nums):
    """
                Q1 + 2*Q2 + Q3
    trimean =   --------------
                      4
    :param nums:
    :return: trimean
    """
    q1 = np.quantile(nums, 0.25)
    q2 = np.quantile(nums, 0.5)
    q3 = np.quantile(nums, 0.75)
    trimean = (q1 + 2.0*q2 + q3)/4.0
    return trimean


def categorical_ratio_feature(nums):
    """
    get the ratio for each category
    :param nums:
    :return:
    """
    c = Counter(nums)
    tot = len(nums)
    percs = []
    for k in c.keys():
        perc = c[k]*1.0/tot
        percs.append(perc)
    return sorted(percs)


def tstd_feature(trimean, nums):
    """
    standard deviation using the tri-mean instead of the mean
    :return:
    """
    seg = 0
    for x in nums:
        seg += (x-trimean)**2

    return math.sqrt(1.0/len(nums) * seg)


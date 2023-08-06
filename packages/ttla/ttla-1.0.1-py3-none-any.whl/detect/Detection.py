from detect.loader import *
from collections import Counter
import math
from commons import CATEGORICAL, ORDINAL, SEQUENTIAL, RATIO_INTERVAL, HIERARCHICAL, COUNTS, OTHER, YEAR
import logging
import numpy as np
from commons.logger import set_config

logger = set_config(logging.getLogger(__name__))

from dateutil import parser


class Detection(object):

    def __init__(self, values):
        self.values = values
        self.cleanValues = self.preprocessing()
        self.conditions = self.check_conditions()
        self.type = self.getType()

    """ check if values nonnegative and real"""
    def check_conditions(self):
        num_vals = len(self.cleanValues)
        grace_percentage = 0.05
        num_neg_float = 0
        new_vals = []
        for k in self.cleanValues:
            if k < 0 or not self.is_int(k):
                num_neg_float+=1
                logger.debug("Breaks the rule of being nonnegative and real: %s, num of vals: %d" % (str(k), num_vals))
                if num_neg_float*1.0/num_vals >= grace_percentage:
                    # logger.debug("negfloat: %d, num_vals: %d, formula: %f" % (num_neg_float,num_vals,(num_neg_float*1.0/num_vals)))
                    return False
            else:
                new_vals.append(k)
        self.cleanValues = new_vals
        # self.values = new_vals
        # for k in self.cleanValues:
        #     print k
        return True

    """ function for cleaning the column """
    def preprocessing(self):
        return commons.get_numerics_from_list(self.values)
        #return self.values

    def getType(self):

        if self.conditions and self.is_ordinal():
            return ORDINAL
        elif self.conditions and self.is_categorical():
            return CATEGORICAL
        elif self.conditions and self.is_sequential():
            return SEQUENTIAL
        elif self.conditions and self.is_hierarchical():
            return HIERARCHICAL
        elif self.conditions and self.is_count():
            return COUNTS
        #else:
        #    return OTHER
        elif self.conditions and self.check_year():
            return YEAR
        else:
            return OTHER

    def check_year(self):
        count_date = 0
        for val in self.cleanValues:
            temp = self.is_date(int(val))
            #print(temp, " -- ", val)
            if temp and len(str(int(val))) == 4 and int(val) <= 2020:
                count_date +=1

        if count_date >= len(self.cleanValues)*0.9:
            return True
        return False

    def is_ordinal(self):
        diffs = [j-i for i, j in zip(self.cleanValues[:-1], self.cleanValues[1:])]
        if all(x == diffs[0] for x in diffs) and self.cleanValues[0] == 1 and diffs[0] != 0:
            return True
        return False

    def is_categorical(self):
        """
        if the given column is categorical or not
        :param col: pandas series
        :return: true of false
        """
        if not self.conditions:
            return False
        cc = Counter(self.cleanValues)
        if len(cc.keys()) <= len(self.cleanValues)**(1/2.0):
        # if len(cc.keys()) <= len(self.cleanValues)**(1/1.5):
            # for k in cc.keys():
            #     if k < 0 or not self.is_int(k):
            #         logger.debug("Not categorical because the value is: %s" % (str(k)))
            #         return False
            return True
        return False

    def is_sequential(self):
        """
        diffs: difference between every two consecutive numbers
        mostPopular: the most popular number in diffs
        true if mostPopular value appears in diffs more or equal times than (int(len(diffs)/2)
        also mostPopular cannot be equal to zero
        """
        diffs = [j-i for i, j in zip(self.cleanValues[:-1], self.cleanValues[1:])]
        mostPopular = max(set(diffs), key=diffs.count)
        if diffs.count(mostPopular) >= (int((len(diffs)+1)/2)) and mostPopular != 0:
            return True
        return False

    def is_hierarchical(self):
        """
        In order to detect hierarchical data in a column we first check the
        number of digits, if it is the same in all the cells, then
        we check if it is not sequential then we consider it to be
        hierarchical. This is if the values are unique; have duplicate values is
        a stron evdence of a non-hierarchical numbers.
        """
        lengths = []
        for i in self.cleanValues:
            lengths.append(len(str(i)))
        mostPopular = max(set(lengths), key = lengths.count)
        if lengths.count(mostPopular) >= (int(len(lengths)*0.99)):
            seen = set()
            if not any(i in seen or seen.add(i) for i in self.cleanValues):
                return True
        return False

    # def is_ratiointerval(self):
    #     nonnegative = sum(1 for number in self.cleanValues if number >= 0)
    #     if len(self.cleanValues) == nonnegative:
    #         if all(isinstance(x, int) for x in self.cleanValues):
    #             if (math.sqrt(max(self.cleanValues)) - math.sqrt(min(self.cleanValues))) > 1:
    #                 return True
    #     return False

    def is_count(self):
        """
        Check if the it represents simple counts
        :return:
        """
        if not self.conditions:
            return False

        q1 = np.quantile(self.cleanValues, q=0.25)
        q2 = np.quantile(self.cleanValues, q=0.5)
        q3 = np.quantile(self.cleanValues, q=0.75)
        p95 = np.quantile(self.cleanValues, q=0.95)
        p_small = np.quantile(self.cleanValues, q=0.05)
        if p_small == 0:
            p_small = np.quantile(self.cleanValues, q=0.1)
            if p_small == 0:
                p_small = 1
        # if p_small == 0 or q2 == 0:
        if q2 == 0:
            q2 = 1
            # return False
        is_outlier = 1.5*(q3-q1) + q3 <= p95
        first_increase = (q2-p_small)*1.0/p_small
        is_first_increase = first_increase >= 2
        second_increase = (p95 - q2)*1.0 / q2
        is_second_increase = second_increase >= 2
        # logger.debug("first: %.3f second: %.3f" % (first_increase, second_increase))
        # logger.debug("is_count check> outlier: %s , first: %s , second: %s" % (str(is_outlier), str(is_first_increase),
        #                                                            str(is_second_increase)))
        #return is_outlier and is_first_increase and is_second_increase
        #return is_outlier and ((is_first_increase and is_second_increase) or (is_second_increase and second_increase > first_increase*2))
        return is_outlier and is_second_increase

    def is_int(self, num):
        return num-int(num) == 0

    def is_date(self, val):
        try:
            value = str(val)
            temp2 = parser.parse(value)
            return temp2
        except:
            return None


def get_num_kind(nums):
    """
    This is used as a wrapper to be called by other models
    :param nums:
    :return:
    """
    d = Detection(nums)
    num_kind = d.getType()
    del d
    return num_kind


def get_kind_and_nums(nums):
    """
    This is used as a wrapper to be called by other models
    :param nums:
    :return:
    """
    d = Detection(nums)
    num_kind = d.getType()
    new_nums = d.cleanValues
    del d
    return num_kind, new_nums

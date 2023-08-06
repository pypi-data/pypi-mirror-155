from detect.loader import *
import os
import pandas as pd
import math
from commons import get_num,  KINDS, get_column_from_meta

from detect.Detection import get_num_kind, get_kind_and_nums, Detection


proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
data_dir = os.path.join(proj_path, 'data')
meta_dir = os.path.join(proj_path, 'meta')


def get_numerics_from_list(nums_str_list):
    """
    :param nums_str_list: list of string or numbers or a mix
    :return: list of numbers or None if less than 50% are numbers
    """
    nums = []
    for c in nums_str_list:
        n = get_num(c)
        if n is not None and not math.isnan(n):
            nums.append(n)
    if len(nums) < len(nums_str_list)/2:
        return None
    return nums


# def get_num(num_or_str):
#     """
#     :param num_or_str:
#     :return: number or None if it is not a number
#     """
#     if isinstance(num_or_str, (int, float)):
#         return num_or_str
#     elif isinstance(num_or_str, basestring):
#         if '.' in num_or_str or ',' in num_or_str or num_or_str.isdigit():
#             try:
#                 return float(num_or_str.replace(',', ''))
#             except Exception as e:
#                 return None


# def get_column_type(filename, columnid):
#     column_type = 'unknown'
#     file_path = os.path.join(data_dir, 'T2Dv2',filename+ '.csv')
#     #file_path = os.path.join(data_dir, 'T2Dv2/') +filename+ '.csv'
#     dftestfile = pd.read_csv(file_path)
#     values = dftestfile.iloc[ : , int(columnid) ]
#
#     numbers_list = get_numerics_from_list(values)
#
#     if numbers_list != None:
#         column_type = get_num_kind(numbers_list)
#     del dftestfile
#     return column_type

def get_column_type(filename, columnid):
    """
    :param filename:
    :param columnid:
    :return: kind/sub-kind
    """
    col = get_column_from_meta(fname=filename, column_id=int(columnid))
    d = Detection(list(col))
    return d.getType()


def overall_evaluation():
    count_successful = 0
    count_failed = 0
    count_overall = 0
    count_year_failed = 0
    count_year_successful = 0
    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
    for index, row in df.iterrows():
        if not math.isnan(row['columnid']):
            #if row['filename'] == '1146722_1_7558140036342906956.tar.gz':
            count_overall += 1
            detected_type = get_column_type(row['filename'], row['columnid'])
            if detected_type == row['kind'] or detected_type == row['sub_kind']:
                count_successful += 1
                if detected_type == 'year':
                    count_year_successful += 1
            else:
                if row['kind'] == 'year' or row['sub_kind'] == 'year':
                    #print("%s | %s | %s - %s / %s" % (row['filename'], row['columnid'], detected_type, row['kind'], row['sub_kind']))
                    count_year_failed += 1
                else:
                    print("%s | %s | %s - %s / %s" % (row['filename'], row['columnid'], detected_type, row['kind'], row['sub_kind']))

                    count_failed += 1
                #print("%s | %s | %s - %s / %s" % (row['filename'], row['columnid'], detected_type, row['kind'], row['sub_kind']))

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("successfully matched: " + str(count_successful))
    print("unsuccessfully matched: " + str(count_failed))

    print("failed year: " + str(count_year_failed))
    print("success year: " + str(count_year_successful))


    print("Overall attempts couter: " + str(count_overall))


# def type_evaluation():
#     # "nominal", "ratio-interval"
#     numerical_types = ["ordinal", "categorical", "sequential", "hierarchical", "random", "count", "other", "year"]
#     count_types = {}
#
#     for nt in numerical_types:
#         count_types[nt] = {'success': 0, 'failure': 0}
#
#     meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
#     df = pd.read_csv(meta_file_dir)
#     for index, row in df.iterrows():
#         if not math.isnan(row['columnid']):
#             detected_type = get_column_type(row['filename'], row['columnid'])
#             if detected_type == row['kind'] or detected_type == row['sub_kind']:
#                 count_types[detected_type]['success'] += 1
#             else:
#                 if row['sub_kind'] == "count":
#                     print row['filename'] + " - " + str(int(row['columnid']))
#
#                 if row['kind'] in count_types:
#                     count_types[row['kind']]['failure'] += 1
#                 else:
#                     count_types[row['sub_kind']]['failure'] += 1
#
#     for key, value in count_types.items():
#         # print(key + ": " + str(value['success']) + " correct out of " + str(value['failure']+value['success']))
#         success = value['success']
#         tot = value['failure']+value['success']
#         if success > 0:
#             prec = success*1.0/tot
#             perc_str = str(round(prec, 3))
#         elif tot == 0:
#             perc_str = "-"
#         else:
#             prec = 0.0
#             perc_str = str(prec)
#         # print("%15s : %3d out of %3d : %.3f" % (key, success, tot, prec))
#         print("%15s : %3d out of %3d : %s" % (key, success, tot, perc_str))


def type_evaluation():
    """
    evaluate the detection
    [X]success: X correctly detected as X
    [X]failure: X incorrectly detect as Y
    [X]invalud: Y incorrectly detect as X
    :return:
    """
    results = {}
    numerical_types = []
    for kind in KINDS:
        if KINDS[kind] == []:
            numerical_types.append(kind)
        else:
            for sub in KINDS[kind]:
                numerical_types.append(sub)

    count_types = {}

    for nt in numerical_types:
        count_types[nt] = {'success': 0, 'failure': 0, 'invalid': 0}

    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
    df = df[df.columnid.notnull()]
    print("shape: "+str(df.shape))

    tot_cols = df.shape[0]

    for index, row in df.iterrows():
        # if True:
        # if not math.isnan(row['columnid']):
        detected_type = get_column_type(row['filename'], row['columnid'])
        if detected_type == row['kind'] or detected_type == row['sub_kind']:
            count_types[detected_type]['success'] += 1
        else:
            # if row['sub_kind'] == "count":
            #     print row['filename'] + " - " + str(int(row['columnid']))

            if row['kind'] in count_types:
                count_types[row['kind']]['failure'] += 1
                count_types[detected_type]['invalid'] += 1

            else:
                count_types[row['sub_kind']]['failure'] += 1
                count_types[detected_type]['invalid'] += 1

    for key, value in count_types.items():
        # print(key + ": " + str(value['success']) + " correct out of " + str(value['failure']+value['success']))
        success = value['success']
        tot = value['failure'] + value['success']
        tot2 = value['invalid'] + value['success']
        if success > 0:
            precision = success * 1.0 / tot
            precision_str = str(round(precision, 3))
            recall = success * 1.0 / tot2
            recall_str = str(round(recall, 3))
            f1 = 2 * precision * recall / (precision + recall)
            f1_str = str(round(f1, 3))
        elif tot == 0 or tot2 == 0:
            if tot == 0:
                precision_str = "-"
                f1_str = "-"
            if tot2 == 0:
                recall_str = "-"
                f1_str = "-"
        else:
            precision = 0.0
            precision_str = str(precision)
            recall = 0.0
            recall_str = str(recall)
            f1_str = "N/A"
        results[key] = {
            "precision": precision_str,
            "recall": recall_str,
            "f1": f1_str
        }
        # print("%15s : %3d out of %3d : %.3f" % (key, success, tot, precision))
        print("%15s : %3d out of (%3d,%3d) : precision %5s,  recall %5s  F1: %5s" % (key, success, tot, tot2, precision_str, recall_str, f1_str))
    print(results)
    return results


    # # verify
    # tot_correct = 0
    # tot_fail = 0
    # tot_invalid = 0
    # for key, value in count_types.items():
    #     tot_correct += value['success']
    #     tot_fail += value['failure']
    #     tot_invalid += value['invalid']
    # print ("total correct: %d\n total fail: %d\n correct_fail: %d\n total: %d" % (tot_correct, tot_fail, tot_correct+tot_fail, tot_cols))


if __name__ == "__main__":
    type_evaluation()

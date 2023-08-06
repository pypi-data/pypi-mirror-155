import os
import pandas as pd
#from .easysparql import *
CACHE_DIR = ".cache"
ENDPOINT = "https://dbpedia.org/sparql"
MIN_NUM_OF_ENT_PER_PROP = 30  # the minimum number of entities per property (get_properties)
QUERY_LIMIT = ""  # At the moment, we do not put any limit on the number of results
MIN_NUM_NUMS = 30  # The minimum number of values that will be annotated, this is to ignore small size

proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

data_dir = os.path.join(proj_path, 'data')
meta_dir = os.path.join(proj_path, 'meta')
models_dir = os.path.join(proj_path, 'local_models')
log_dir = os.path.join(proj_path, 'local_logs')


# kinds
NOMINAL = "nominal"
ORDINAL = "ordinal"
RATIO_INTERVAL = "ratio-interval"

# sub kinds
CATEGORICAL = "categorical"
SEQUENTIAL = "sequential"
HIERARCHICAL = "hierarchical"
RANDOM = "random"
COUNTS = "count"
OTHER = "other"

YEAR = "year"


# I am not sure of the below is useful
# kinds and subkinds
KINDS = {
    ORDINAL: [],
    NOMINAL: [CATEGORICAL, SEQUENTIAL, HIERARCHICAL, RANDOM],
    RATIO_INTERVAL: [COUNTS, OTHER],
    YEAR: []
}


def get_column_from_meta(fname, column_id):
    """
    :param fname:
    :param column_id:
    :return:
    """
    fdir = os.path.join(data_dir, 'T2Dv2', fname+".csv")
    df = pd.read_csv(fdir)
    col_name = df.columns.values[column_id]
    return list(df[col_name])


def t2dv2_columns_of_kind(num_kind, sub_kind=None):
    """
    :param num_kind: nominal, ordinal, ratio-interval
    :return: a dataframe of the specified kind
    """
    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
    if sub_kind is None:
        dfkind = df[df.kind == num_kind]
    else:
        dfkind = df[df.kind == num_kind and df.sub_kind == sub_kind]
    print(dfkind)
    return dfkind


def get_numerics_from_list(nums_str_list):
    """
    :param nums_str_list: list of string or numbers or a mix
    :return: list of numbers or None if less than 50% are numbers
    """
    nums = []
    for c in nums_str_list:
        n = get_num(c)
        if n is not None:
            nums.append(n)
    if len(nums) < len(nums_str_list)/2:
        return None
    return nums


def get_num(num_or_str):
    """
    :param num_or_str:
    :return: number or None if it is not a number
    """
    if pd.isna(num_or_str):
        return None
    elif isinstance(num_or_str, (int, float)):
        return num_or_str
    elif isinstance(num_or_str, str):
        if '.' in num_or_str or ',' in num_or_str or num_or_str.isdigit():
            try:
                return float(num_or_str.replace(',', ''))
            except Exception as e:
                return None
    return None


def class_uri_to_fname(class_uri):
    """
    :param class_uri:
    :return:
    """
    if class_uri[:7] == "http://":
        class_dname = class_uri[7:]
    elif class_uri[:8] == "https://":
        class_dname = class_uri[8:]
    class_fname = class_dname.replace('/', '__').replace(',', '').replace('#', '_')#.replace('-', '_')
    return class_fname

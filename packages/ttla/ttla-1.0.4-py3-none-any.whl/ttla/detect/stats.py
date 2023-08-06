from loader import *
from commons import meta_dir
import pandas as pd
from commons import KINDS, YEAR
from collections import Counter
from pprint import PrettyPrinter


def compute_stats():
    meta_file_dir = os.path.join(meta_dir, 'T2Dv2_typology.csv')
    df = pd.read_csv(meta_file_dir)
#    dfkind = df[df.kind.notnull()]
    dfkind = df[df.columnid.notnull()]
    # if sub_kind is None:
    #     dfkind = df[df.kind == num_kind]
    # else:
    #     dfkind = df[df.kind == num_kind and df.sub_kind == sub_kind]
    # print(dfkind)
    # return dfkind
    print(dfkind.shape)
    ckind = Counter(dfkind['kind'])
    csub = Counter(dfkind['sub_kind'])
    print(ckind)
    print(csub)
    tot = dfkind.shape[0]
    stats = dict()
    for kind in KINDS.keys():
        d = {
            'num': ckind[kind],
            'per': ckind[kind] * 1.0 / tot,
        }
        stats[kind] = d

        if KINDS[kind] != []:
            for sub in KINDS[kind]:
                d = {
                    'num': csub[sub],
                    'per': csub[sub]*1.0/tot,
                }
                stats[sub] = d
    for k in stats.keys():
        stats[k]['per'] = round(stats[k]['per'], 3)

    pp = PrettyPrinter(indent=4)
    pp.pprint(stats)
    # print stats


if __name__ == "__main__":
    compute_stats()


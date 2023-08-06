import sys
from loader import *
import commons


def print_help():
    help_msg = """TEST:
    t2dv2
    olympic
    
To Run the labeling:
    python cmd.py TEST
    """
    print(help_msg)


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        test_name = sys.argv[1]
    else:
        test_name = "few args"

    if test_name == 't2dv2':
        # commons.t2dv2_columns_of_kind("nominal")
        for kind in commons.KINDS:
            for sub in commons.KINDS[kind]:
                commons.t2dv2_columns_of_kind(kind, sub)
        # print("T2Dv2 test is still under construction")
    elif test_name == 'olympic':
        print("Olympic Games test is under construction")
    else:
        print_help()

import sys
import os
proj_path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
# print("detect init project path: "+str(proj_path))
sys.path.append(proj_path)
import commons

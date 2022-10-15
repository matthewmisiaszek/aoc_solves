import sys
import os
root_path = os.path.dirname(os.path.dirname(__file__))
print(root_path)
# root_path = os.path.abspath('..')
if root_path not in sys.path:
    sys.path.append(root_path)

from common.dancer import *
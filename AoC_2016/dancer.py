import sys
import os
root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)

from common.dancer import *
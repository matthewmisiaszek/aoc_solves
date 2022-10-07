"""Directory Augmentation and Normalized Code Execution Routine"""
import sys
import os
root_path = os.path.abspath('.')
if root_path not in sys.path:
    sys.path.append(root_path)

from common.dancer import *
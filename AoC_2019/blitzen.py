"""Boilerplate Library for Inputs, Timing, and Zealous Execution Normalization (BLITZEN)"""

import sys
import os
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root_path not in sys.path:
    sys.path.append(root_path)

from donner.blitzen import *
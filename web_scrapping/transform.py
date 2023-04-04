import os
import re
import pandas as pd

from ast import literal_eval

# Relative paths
CURRENT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CURRENT)
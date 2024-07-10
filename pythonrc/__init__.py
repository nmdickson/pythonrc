'''This package should be imported by a $PYTHONSTARTUP file.
We provide a ../src.py file which does that, but you can also make your own
if this package is installed.
'''

# --------------------------------------------------------------------------
# import pythonrc modules
# --------------------------------------------------------------------------

from .plotting import *
from .numbers import *

# --------------------------------------------------------------------------
# Common useful packages
# --------------------------------------------------------------------------

import os, sys, glob, pathlib, logging, warnings
from importlib import reload

warnings.simplefilter('always')  # don't go silently into that sweet bug

try:
    logging.getLogger().setLevel('DEBUG')
except:
    raise RuntimeError("Couldn't raise root logger level")

try:
    import numpy as np
except ImportError as err:
    raise err

try:
    import matplotlib.pyplot as plt
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('PIL').setLevel(logging.WARNING)
except ImportError as err:
    raise err

try:
    import astropy.units as u
except ImportError as err:
    raise err

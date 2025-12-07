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


import os, sys, glob, pathlib, logging, warnings, pprint
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


# --------------------------------------------------------------------------
# QoL functions
# --------------------------------------------------------------------------


class _ANSIColours:

    @property
    def available(self):
        return ({attr for attr in self.__dir__() if not attr.startswith('_')}
                - {"available"})

    # normal
    black = "\033[0;30m"
    red = "\033[0;31m"
    green = "\033[0;32m"
    yellow = "\033[0;33m"
    blue = "\033[0;34m"
    purple = "\033[0;35m"
    cyan = "\033[0;36m"
    white = "\033[0;37m"

    # bold
    black_bf = "\033[1;30m"
    red_bf = "\033[1;31m"
    green_bf = "\033[1;32m"
    yellow_bf = "\033[1;33m"
    blue_bf = "\033[1;34m"
    purple_bf = "\033[1;35m"
    cyan_bf = "\033[1;36m"
    white_bf = "\033[1;37m"

    # underline
    black_ul = "\033[4;30m"
    red_ul = "\033[4;31m"
    green_ul = "\033[4;32m"
    yellow_ul = "\033[4;33m"
    blue_ul = "\033[4;34m"
    purple_ul = "\033[4;35m"
    cyan_ul = "\033[4;36m"
    white_ul = "\033[4;37m"

    # background
    black_bg = "\033[40m"
    red_bg = "\033[41m"
    green_bg = "\033[42m"
    yellow_bg = "\033[43m"
    blue_bg = "\033[44m"
    purple_bg = "\033[45m"
    cyan_bg = "\033[46m"
    white_bg = "\033[47m"

    # high intensity
    black_hi = "\033[0;90m"
    red_hi = "\033[0;91m"
    green_hi = "\033[0;92m"
    yellow_hi = "\033[0;93m"
    blue_hi = "\033[0;94m"
    purple_hi = "\033[0;95m"
    cyan_hi = "\033[0;96m"
    white_hi = "\033[0;97m"

    # bold high intensity
    black_bfhi = "\033[1;90m"
    red_bfhi = "\033[1;91m"
    green_bfhi = "\033[1;92m"
    yellow_bfhi = "\033[1;93m"
    blue_bfhi = "\033[1;94m"
    purple_bfhi = "\033[1;95m"
    cyan_bfhi = "\033[1;96m"
    white_bfhi = "\033[1;97m"

    # high intensity backgrounds
    black_bghi = "\033[0;100m"
    red_bghi = "\033[0;101m"
    green_bghi = "\033[0;102m"
    yellow_bghi = "\033[0;103m"
    blue_bghi = "\033[0;104m"
    purple_bghi = "\033[0;105m"
    cyan_bghi = "\033[0;106m"
    white_bghi = "\033[0;107m"

    reset = "\033[0m"


COLOURS = _ANSIColours()


def in_colour(st, colour):
    return f"{getattr(COLOURS, colour)}{st}{COLOURS.reset}"


def ls():
    import __main__
    import shutil
    import textwrap as tw

    names = sorted([nm for nm in __main__.__dict__ if not nm.startswith('_')])

    max_n = len(max(names, key=lambda t: len(t)))

    cmap = {
        "module": "cyan_bf",
        "function": "red_bf"
    }

    # Get first wrap to decide rows (pad with '-' to avoid wrapping)
    rows = tw.wrap('  '.join([
        f"{nm:-<{max_n}}"for nm in names
    ]), width=shutil.get_terminal_size().columns - 1, break_long_words=False)

    # unpack each item (column) for the rows
    for line in rows:
        cols = [nm.strip('-') for nm in line.split()]
        types = [type(__main__.__dict__[nm]).__name__ for nm in cols]

        # write out the row with colours added
        sys.stdout.write('  '.join(
            [in_colour(f"{nm:<{max_n}}", cmap.get(tp, 'white_bf'))
             for nm, tp in zip(cols, types)]
        ))

        sys.stdout.write('\n')


def ll():
    import __main__

    names = sorted(__main__.__dict__)
    items = [__main__.__dict__[nm] for nm in names]
    types = [type(obj).__name__ for obj in items]

    for ind, obj in enumerate(items):
        if types[ind] != 'module':  # to avoid module with shape method
            try:
                shp = str(obj.shape)
            except AttributeError:
                try:
                    shp = f'({len(obj)})'
                except TypeError:
                    shp = ''

            types[ind] += shp

    max_n = len(max(types, key=lambda t: len(t)))

    cmap = {
        "module": "cyan_bf",
        "function": "red_bf"
    }

    for nm, tp, obj in zip(names, types, items):

        clr_nm = in_colour(nm, cmap.get(tp, 'white_bf'))

        size, unit = sys.getsizeof(obj), ' '

        if 1e9 < size < 1e12:
            size = size / 1e9
            unit = 'G'
        elif 1e6 < size < 1e9:
            size = size / 1e6
            unit = 'M'
        elif 1e3 < size < 1e6:
            size = size / 1e3
            unit = 'K'

        size_nm = f'{f"{size:3.1f}" if size < 10 else f"{int(size):3d}"}{unit}'

        sys.stdout.write(f"{tp:>{max_n}} "
                         f"{size_nm} "
                         f"{clr_nm}\n")

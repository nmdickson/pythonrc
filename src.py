try:
    # Try it the right way

    from pythonrc import *

except ImportError:
    # If that fails, force it to behave

    import sys, inspect, pathlib

    sys.path.append(
        pathlib.Path(inspect.getfile(inspect.currentframe())).parent
    )

    from pythonrc import *


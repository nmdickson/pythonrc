'''Numerical helper functions'''


__all__ = ['equal_eps', 'multerr', 'diverr']


def equal_eps(arr, true_arr, dtype=None):
    '''determine if all values of two arrays are within the dtype epsilon'''
    import numpy as np

    if dtype is None:
        dtype = arr.dtype

    return np.all(np.abs(arr - true_arr) < np.finfo(dtype).eps)


def multerr(x, σx, y, σy):
    '''Multiply two values/arrays and propogate the gaussian errors'''
    import numpy as np

    err = np.sqrt((σx * y)**2 + (σy * x)**2)

    return x * y, err


def diverr(x, σx, y, σy):
    '''Divide two values/arrays and propogate the gaussian errors'''
    import numpy as np

    err = np.sqrt((σx / y)**2 + (-x * σy / y**2)**2)

    return x / y, err

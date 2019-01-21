""" This module provides helper functions used in manipulating hypercubes.
"""

import numpy as np
from typing import Union, Iterable

def slice_ndarray(arr: np.ndarray, axes: Union[int, Iterable[int]], 
                inds: Union[int, Iterable[int]]) -> np.ndarray:
    """ Returns a slice of an array. 

    Parameters
    ----------
    arr : numpy.ndarray
        The array to be sliced
    axes : Union[int, Iterable[int]]
        The axes that are fixed
    inds : Union[int, Iterable[int]]
        The indices corresponding to the fixed axes

    Returns
    -------
    numpy.ndarray:
        A view of a slice of `arr`.

    Raises
    ------
    ValueError
        If length of `axes` is not equal to length of `inds`

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(8).reshape(2, 2, 2)
    >>> arr
    array([[[0, 1],
            [2, 3]],
    <BLANKLINE>
           [[4, 5],
            [6, 7]]])
    >>> slice_ndarray(arr, 0, 0)
    array([[0, 1],
           [2, 3]])
    >>> slice_ndarray(arr, (1, 2), (0, 0))
    array([0, 4])
    """

    # create a list of slice objects, one for each dimension of the array
    # Note: slice(None) is the same as ":". E.g. arr[:, 4] = arr[slice(none), 4)]
    sl = [slice(None)] * arr.ndim    
    try:
        # first assume axes and inds are iterable and not single integers
        if len(axes) != len(inds):
            raise ValueError("axes and inds must be of the same length")

        for axis, ind in zip(axes, inds):
            sl[axis] = ind
    except: 
        # perhaps axes and inds are integers
        sl[axes] = inds

    return arr[tuple(sl)]



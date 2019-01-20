""" This module provides helper functions used in manipulating hypercubes.
"""

import numpy as np
from typing import List, Callable, Union, Iterable, Tuple, Any

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


def insert_into_tuple(tup: Tuple, pos: Union[int, Iterable[int]], 
                      val: Union[Any, Iterable[Any]]) -> Tuple:
    """ Insert values into a tuple. 

    Parameters
    ----------
    tup : tuple
        the tuple into which values are to be inserted
    pos : Union[int, Iterable[int]]
        The positions into which values are to be inserted
    val : Union[Any, Iterable[Any]]
        The values corresponding to the positions in `pos`

    Returns
    -------
    Tuple:
        A copy of `tup` with values inserted.

    Raises
    ------
    ValueError
        If length of `pos` is not equal to length of `val`

    See Also
    --------
    list.insert
 
    Notes
    -----
    `tup` is converted to a list and the list.insert method is used to
    insert values. the list is then converted to a tuple and returned.

    Examples
    --------
    >>> tup = (0, 1, 2, 3)
    >>> pos = (5, 1)
    >>> val = (9, 8)
    >>> insert_into_tuple(tup, pos, val)
    (0, 8, 1, 2, 3, 9)
    >>> insert_into_tuple(tup, (), ())
    (0, 1, 2, 3)
    """

    tl = list(tup)

    try:
        # first assume pos and val are iterable and not single integers
        if len(pos) != len(val):
            raise ValueError("pos and val must be of the same length")
        
        if len(pos) == 0:
            return tup

        # sort pos so from low to high; sort val correspondingly
        stl = list(zip(*sorted(zip(pos, val))))
        for p, v in zip(stl[0], stl[1]):
            tl.insert(p, v)
    except: 
        # perhaps pos and cal are integers
        tl.insert(pos, val)

    return tuple(tl)


def unique(it: Iterable[Any]) -> bool:
    """ check if all elements of an iterable of unqiue

    Parameters
    ----------
    it : Iterable[Any]
        The iterable to be checked for unique elements

    Returns
    -------
    bool:
        True if all elements of `it` of unique; False otherwise
 
    Notes
    -----
    Iterates over every element until a match is found (or not
    found if all elements are unique).
    If the elements of `it` are hashable then code such as
    len(it) == len(set(it)) is more more efficient.
  
    Examples
    --------
    >>> it = [[0, 1], [0,2], [0,1]]
    >>> unique(it)
    False
    >>> it = [[0, 1], [0,2], [1,2]]
    >>> unique(it)
    True
    """

    seen = []
    return not any(i in seen or seen.append(i) for i in it)





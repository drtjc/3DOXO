import numpy as np
import itertools as it
from pprint import pprint
from scipy.special import comb
from typing import List, Callable, Union



def slice_plane(arr, axes, inds):
    if len(axes) != len(inds):
        raise ValueError("axes and inds must be of the same length")

    sl = [slice(None)] * arr.ndim    
    try:
        for axis, ind in zip(axes, inds):
            sl[axis] = ind
    except: # axes and inds contain only 1 value
        sl[axes] = inds
    return arr[tuple(sl)]








size = 4
dim = 3

arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
#arr = np.zeros([size] * dim, int)




def lm(s, d):
    l = 0
    for i in range(1,d + 1):
        l += comb(d, i, True) * (s ** (d-i)) * (2 ** (i - 1)) 
    return l




def get_diagonals() -> Callable[[numpy.ndarray], List[numpy.ndarray]]:
    """ Returns a function that calculates the diagonals of an array. 
    The returned function has the following structure:

    Parameters
    ----------
    arr : numpy.ndarray
        `arr` is the array whose diagonals are to be calculated

    Returns
    -------
    list:
        A list of numpy.ndarray views of the diagonals of `arr`.

    Notes
    -----
    Let d be the number of dimensions of `arr`.
    
    The number of corners is of `arr` is 2^d - a line has 2 corners, 
    a square 4, a cube 8, a tesseract 16, ...
    
    The number of diagonals is 2^d / 2 since two connecting 
    corners form a line. 

    Example
    -------
    >>> import numpy as np
    >>> arr = np.arange(8).reshape(2, 2, 2)
    >>> arr
    array([[[0, 1],
            [2, 3]],
    <BLANKLINE>
           [[4, 5],
            [6, 7]]])
    >>> diagonals = get_diagonals()
    >>> diags = diagonals(arr)
    >>> diags
    [array([0, 7]), array([1, 6]), array([4, 3]), array([5, 2])]
    >>> arr[0, 0, 0] = 99
    >>> diags
    [array([99,  7]), array([1, 6]), array([4, 3]), array([5, 2])]
    """

    diags = []
    
    def diagonals(arr: numpy.ndarray) -> List[numpy.ndarray]:
        if arr.ndim == 1:
            diags.append(arr)
        else:
            diagonals(arr.diagonal())
            diagonals(np.flip(arr, 0).diagonal())
        return diags

    return diagonals


def lines(arr: numpy.ndarray, flatten: bool = True) -> Union[List[numpy.ndarray], List[List[numpy.ndarray]]]: 
    lines = [] # list of ndarray or list of list of ndarrays
    diagonals = get_diagonals()

    # loop over the numbers of dimensions of the plane in which the line exists
    for i in range(dim): 
        # loops over all planes of i dimensions
        for j in it.combinations(range(dim), r = i + 1): 
            # the other dimensions can assume any position from a combination of all positions
            for position in it.product(range(size), repeat = dim - i - 1):
                # take a slice in plane j given position
                sl = slice_plane(arr, set(range(dim)) - set(j), position)
                # get all possible lines from slice
                diags = diagonals(sl)
                lines.extend(diags) if flatten else lines.append(diags) 
    return lines





#arr[0,0,0] = 999
l = lines(arr)
#pprint(l)
#print(arr)
#pprint(l)

#print(lm(size, dim))

#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
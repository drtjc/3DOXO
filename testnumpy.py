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








size = 5
dim = 4

arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
#arr = np.zeros([size] * dim, int)




def lm(s, d):
    l = 0
    for i in range(1,d + 1):
        l += comb(d, i, True) * (s ** (d-i)) * (2 ** (i - 1)) 
    return l




def get_diagonals() -> Callable[[np.ndarray], List[np.ndarray]]:
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

    ###TJC but can't call diagonals again as list is not empty i.e maintains state

    >>> diags
    [array([0, 7]), array([1, 6]), array([4, 3]), array([5, 2])]
    >>> arr[0, 0, 0] = 99
    >>> diags
    [array([99,  7]), array([1, 6]), array([4, 3]), array([5, 2])]
    """
    
    # create list to store diagonals
    diags = []
    
    # the diagonals function is recursive. How it works is best shown by example:
    # 1d: arr = [0, 1] then the diagonal is also [0, 1].
    
    # 2d: arr = [[0, 1],
    #            [2, 3]]
    # The numpy diagonal method gives the main diagonal = [0, 3], a 1d array
    # which is recursively passed to the diagonals function.
    # To get the opposite diagonal we first use the numpy flip function to
    # reverse the order of the elements along the given dimension, 0 in this case.
    # This gives [[2, 3],
    #              0, 1]]
    # The numpy diagonal method gives the main diagonal = [2, 1], a 2d array
    # which is recursively passed to the diagonals function.

    # 3d: arr = [[[0, 1],
    #             [2, 3]],
    #            [[4, 5],
    #             [6, 7]]]
    #

    # 4d: 

    def diagonals(arr: np.ndarray) -> List[np.ndarray]:
        if arr.ndim == 1:
            diags.append(arr)
        else:
            diagonals(arr.diagonal())
            diagonals(np.flip(arr, 0).diagonal())
        return diags

    return diagonals




def lines(arr: np.ndarray, flatten: bool = True) -> Union[List[np.ndarray], List[List[np.ndarray]]]: 
    lines = [] # list of ndarray or list of list of ndarrays

    # loop over the numbers of dimensions of the plane in which the line exists
    for i in range(dim): 
        # loops over all planes of i dimensions
        for j in it.combinations(range(dim), r = i + 1): 
            # the other dimensions can assume any position from a combination of all positions
            for position in it.product(range(size), repeat = dim - i - 1):
                # take a slice in plane j given position
                sl = slice_plane(arr, set(range(dim)) - set(j), position)
                # get all possible lines from slice
                diags = get_diagonals()(sl)
                lines.extend(diags) if flatten else lines.append(diags) 
    return lines




#print(arr)
#arr[0,0,0] = 999
l = lines(arr, True)
pprint(len(l))
#tt = get_diagonals()(arr)
#print(tt)

#pprint(l)

print(lm(size, dim))

#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
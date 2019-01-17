import numpy as np
import itertools as it
from scipy.special import comb
from typing import List, Callable, Union, Iterable

from pprint import pprint


def slice_plane(arr: np.ndarray, axes: Union[int, Iterable[int]], 
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
    >>> slice_plane(arr, 0, 0)
    array([[0, 1],
           [2, 3]])
    >>> slice_plane(arr, (1, 2), (0, 0))
    array([0, 4])
    """

    # create a list of slice objects, one for each dimension of the array
    # slice(None) is the same as ":".
    # E.g. arr[:, 4] = arr[slice(none, 4)]
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




dim = 3
size = 4


arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
#arr = np.zeros([size] * dim, int)




def num_lines(*, dim: int, size: int) -> int:
    count = 0
    for i in range(1, dim + 1):
        count += comb(dim, i, True) * (size ** (dim - i)) * (2 ** (i - 1)) 
    return count




def get_diagonals() -> Callable[[np.ndarray], List[np.ndarray]]:
    """ Returns a function that calculates the diagonals of an array. 
    The returned function has the following structure:

    Parameters
    ----------
    arr : numpy.ndarray
        The array whose diagonals are to be calculated

    Returns
    -------
    List[numpy.ndarray] :
        A list of numpy.ndarray views of the diagonals of `arr`.

    Notes
    -----
    Let d be the number of dimensions of `arr`.
    
    The number of corners is of `arr` is 2^d - a line has 2 corners, 
    a square 4, a cube 8, a tesseract 16, ...
    
    The number of diagonals is 2^d / 2 since two connecting 
    corners form a line. 

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
    >>> diagonals = get_diagonals()
    >>> diags = diagonals(arr)
    >>> diags
    [array([0, 7]), array([1, 6]), array([4, 3]), array([5, 2])]
    >>> arr[0, 0, 0] = 99
    >>> diags
    [array([99,  7]), array([1, 6]), array([4, 3]), array([5, 2])]

    Note that the diagonals function returned by get_diagonals maintains
    the list of digonals returned between invocations.
    >>> arr = np.arange(2)
    >>> arr
    array([0, 1])
    >>> diagonals = get_diagonals()
    >>> diags = diagonals(arr)
    >>> diags
    [array([0, 1])]
    >>> diags = diagonals(arr)
    >>> diags
    [array([0, 1]), array([0, 1])]

    Call get_diagonals again in order to clear the list of 
    returned diagonals.
    >>> get_diagonals()(arr)
    [array([0, 1])]
    >>> get_diagonals()(arr)
    [array([0, 1])]
    """
    
    # create list to store diagonals
    diags = []
    
    # The diagonals function is recursive. How it works is best shown by example.
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
    # The numpy diagonal method gives the main diagonals in the 3rd dimension
    # as rows.
    #            [[0, 6],
    #             [1, 7]]
    # Note that the diagonals of this array are [0, 7] and [6, 1] which are
    # retrieved by a recurive call to the diagonals function.
    # We now have 2 of the 4 diagonals of the orginal 3d arr.
    # To get the opposite diagonals we first use the numpy flip function which
    # gives
    #           [[[4, 5],
    #             [6, 7]],
    #            [[0, 1],
    #             [2, 3]]]
    # and a call to the numpy diagonal method gives
    #            [[4, 2],
    #             [5, 3]]
    # The diagonals of this array are [4, 3] and [2, 5]
    # We now have all 4 diagonals of the original 3d arr.

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

#print(len(set(l)))

#pprint(l)

print(num_lines(dim = dim, size = size))

#if __name__ == "__main__":
#    import doctest
#    doctest.testmod()
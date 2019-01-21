""" Provides functionalilty for working with celled hypercubes.

Hypercubes are extensions of lines, squares and cubes into higher dimensions.
Celled hypercubes can be thought as a grid or lattice structure.
From this point, hypercubes is used to mean celled hypercubes.

A celled hypercube can be described by its dimension and the number of
cells in any dimension. We denote this as h(d, n).
For example: h(2, 3) is a 3x3 grid; h(3, 4) is a 4x4x4 lattice.
A hypercube of dimension d may also be referred to as a d-cube.

A cell's position can be specified in coordinate style. 
For example, given h(3, 4) then some valid coordinates are (1,1,1), 
(2,1,3) and (4,4,4).

The term m-agonal is a shortened function version of 
"m-dimensional diagonal". So in 3-cube you would find a 1-agonal, 2-agonal
and 3-agonal. A 1-agonal is customarily known as a row, column or pillar. 
If 3 coordinates change in an 5-cube, while the others remain constant, this
constitutes a 3-agonal.
For a given h(d, n), 1 <= m <= n, a m-agonal always has n cells.

The term line is used to refer to any m-agonal in general

This module uses a numpy.ndarray to represent celled hypercubes.
The following functions are provided:

num_lines: 
    Calculate the number of lines in a hypercube.

get_diagonals:


get_lines:


get_cells_lines:


slide_ndarray:


"""

# do all as generator????


import numpy as np #type: ignore
import itertools as it
from scipy.special import comb #type: ignore
from collections import defaultdict
from typing import List, Callable, Union, Collection, Tuple, Any, DefaultDict
Lines = List[np.ndarray]  # call this Line
## change docstring to reflect alias, # choose name different from lines (since used for diagonals)

def num_lines(dim: int, size: int) -> int:  # use d and n
    """ Calculate the number of lines in a hypercube.  

    Parameters
    ----------
    dim : int
        The number of dimensions of the hypercube
    size : int
        The size of the hypercube (number of cells in any dimension)
 
    Returns
    -------
    int:
        The number of lines, including diagonals, in a hypercube.

    Notes
    -----
    Let d be the number of dimensions and s the size.
    Let n be the number of lines, including diagonals. Then

        n = sum{i=1, i=d} [ dCi * s^(d-i) * (2^i)/2 ]

    where dCi is 'd choose i'.

    Sketch of proof:
    Let n_i be the number of lines that exist in exactly i dimensions.
    For example, consider the following square:

        [[0, 1],
         [2, 3]]

    The lines that exist in one dimension are [0, 1], [2, 3], 
    [0, 2] and [1, 3] and n_1 = 4.  

    The lines that exist in two dimesions are [0, 3] and [1, 2] 
    and n_2 = 2.
    
    Hence n = n_1 + n_2 = 6

    It is trivially true that the n is the sum of n_i, i.e.,

        n = sum{i=1, i=d} n_i

    Next we show how n_i can be calculated.
    The number of ways of choosing i dimensions from d is dCi.
    For example if d=3 and i=2, then the 3 combinations of 
    2 dimensions (squares) are (1, 2), (1, 3) and (2, 3).

    The number of remaining dimensions is d-i, and the number of cells
    in these dimensions is s^(d-i). Any cell could be selected extracting
    an i-dimensional hypercube.

    For any one of the possible combinations of i-dimensional
    hypercubes, the number of corners is 2^i. A line has 2 corners,
    a square 4, a cube 8, a tesseract 16, ...
    Since a line connects 2 corners, the number of lines is (2^i)/2.

    Examples
    --------
    >>> num_lines(dim = 2, size = 3)
    8
    >>> num_lines(dim = 3, size = 4)
    76
    """

    count = 0
    for i in range(1, dim + 1):
        count += comb(dim, i, True) * (size ** (dim - i)) * (2 ** (i - 1)) 
    return count


def get_diagonals() -> Callable[[np.ndarray], Lines]:
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

    def diagonals(arr: np.ndarray) -> Lines:
        if arr.ndim == 1:
            diags.append(arr)
        else:
            diagonals(arr.diagonal())
            diagonals(np.flip(arr, 0).diagonal())
        return diags

    return diagonals


def get_lines(arr: np.ndarray, flatten: bool = True) -> \
              Tuple[Union[Lines, List[Lines]], int]: 
    """ Returns the lines, including diagonals, in an array

    Parameters
    ----------
    arr : numpy.ndarray
        The array whose lines are to be calculated

    flatten : bool, optional 
        Determines if the lines are returned as a flat list, or
        nested list in which each sublist contains lines that exist
        in the same number of dimension i.e, 1-dimensional lines,
        2-dimensional lines, etc.
        A flat list is return by default.

    Returns
    -------
    Union[List[np.ndarray], List[List[np.ndarray]] :
        A list of numpy.ndarray views of the lines in `arr`.
        The `argument` determines if the list is flat or sublisted by 
        the dimensional extent of the lines.
    int :
        The number of lines. 
            
    Raises
    ------
    AssertionError
        If number of lines returned by this function does not
        equal that calculated by the num_lines function.
        THIS IS A CRITCAL ERROR THAT MEANS THIS FUNCTION HAS
        A FLAWED IMPLEMENTATION.
    
    See Also
    --------
    num_lines
    get_diagonals

    Notes
    -----
    The notes section for the function num_lines provides a sketch of a 
    constructive proof for the number of lines in a hypercube. This has
    been used to implement this function. 

    Examples
    --------
    >>> import numpy as np
    >>> arr = np.arange(4).reshape(2, 2)
    >>> arr
    array([[0, 1],
           [2, 3]])
    >>> lines, count = get_lines(arr)
    >>> lines
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> count
    6
    >>> len(lines)
    6
    >>> arr[0, 0] = 99
    >>> lines
    [array([99,  2]), array([1, 3]), array([99,  1]), array([2, 3]), array([99,  3]), array([2, 1])]
    >>> arr[0, 0] = 0
    >>> lines, count = get_lines(arr, False)
    >>> lines
    [[array([0, 2])], [array([1, 3])], [array([0, 1])], [array([2, 3])], [array([0, 3]), array([2, 1])]]
    >>> count
    6
    >>> len(lines)
    5
    """
    
    dim = arr.ndim
    size = arr.shape[0]
    lines = []
    count = 0

    # loop over the numbers of dimensions in which the line exists
    for i in range(dim): 
        # loop over all possible combinations of i-dimensional hypercubes
        for j in it.combinations(range(dim), r = i + 1): 
            # the other dimensions can assume any position from a combination of all positions
            for position in it.product(range(size), repeat = dim - i - 1):
                # take a slice in plane j given position
                sl = slice_ndarray(arr, set(range(dim)) - set(j), position)
                # get all possible lines from slice
                diags = get_diagonals()(sl)
                count += len(diags)
                if flatten:
                    lines.extend(diags)
                else:
                    lines.append(diags)
    
    assert count == num_lines(dim, size)
    return lines, count


def get_cells_lines(lines: Lines, dim: int) -> \
                    DefaultDict[Tuple[int], Lines]:
    """ Returns the lines intersected by each cell in a hypercube

    Parameters
    ----------
    lines : List[np.ndarray]
        The first returned value from get_lines(arr) where arr is of the
        form np.arange(size ** dim, dtype = int).reshape([size] * dim).
        That is, arr is populated with the values 0,1,2,...,size^dim - 1.

    dim : int 
        The dimension of the array (hypercube) that was used to
        generate the `lines` parameter.

    Returns
    -------
    DefaultDict[Tuple[int], List[np.ndarray]] :
        A dictionary with keys equal to possible cell position of the
        hypercube represented as a tuple. For each cell key, the value is 
        a list of numpy.ndarray views that are lines containing the cell.
            
    See Also
    --------
    get_lines

    Notes
    -----
    The implementation of this function uses np.unravel_index, and relies
    uopn the lines parameter being generated from an array populated with
    values 0,1,2,...
 
    Examples
    --------
    >>> import numpy as np
    >>> from pprint import pprint
    >>> arr = np.arange(4).reshape(2, 2)
    >>> arr
    array([[0, 1],
           [2, 3]])
    >>> lines, _ = get_lines(arr)
    >>> lines
    [array([0, 2]), array([1, 3]), array([0, 1]), array([2, 3]), array([0, 3]), array([2, 1])]
    >>> cells_lines = get_cells_lines(lines, dim = 2)
    >>> pprint(cells_lines) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
               {(0, 0): [array([0, 2]), array([0, 1]), array([0, 3])],
                (0, 1): [array([1, 3]), array([0, 1]), array([2, 1])],
                (1, 0): [array([0, 2]), array([2, 3]), array([2, 1])],
                (1, 1): [array([1, 3]), array([2, 3]), array([0, 3])]})
    >>> arr[0, 0] = 99
    >>> pprint(cells_lines) #doctest: +NORMALIZE_WHITESPACE
    defaultdict(<class 'list'>,
                {(0, 0): [array([99,  2]), array([99,  1]), array([99,  3])],
                (0, 1): [array([1, 3]), array([99,  1]), array([2, 1])],
                (1, 0): [array([99,  2]), array([2, 3]), array([2, 1])],
                (1, 1): [array([1, 3]), array([2, 3]), array([99,  3])]})  
    """
    
    size = lines[0].size
    shape = [size] * dim
    cells_lines: DefaultDict = defaultdict(list)

    for line in lines:
        for j in range(size):
            cell_inds = np.unravel_index(line[j], shape)
            cells_lines[cell_inds].append(line) 
    return cells_lines


def slice_ndarray(arr: np.ndarray, axes: Collection[int], 
                inds: Collection[int]) -> np.ndarray:
    """ Returns a slice of an array. 

    Parameters
    ----------
    arr : numpy.ndarray
        The array to be sliced
    axes : Iterable[int]
        The axes that are fixed
    inds : Iterable[int]
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
    >>> slice_ndarray(arr, (0,), (0,))
    array([[0, 1],
           [2, 3]])
    >>> slice_ndarray(arr, (1, 2), (0, 0))
    array([0, 4])
    """

    # create a list of slice objects, one for each dimension of the array
    # Note: slice(None) is the same as ":". E.g. arr[:, 4] = arr[slice(none), 4)]
    sl: List[Union[slice, int]] = [slice(None)] * arr.ndim    
    if len(axes) != len(inds):
        raise ValueError("axes and inds must be of the same length")
    
    for axis, ind in zip(axes, inds):
        sl[axis] = ind
    
    return arr[tuple(sl)]










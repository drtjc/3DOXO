def diagonals_inds(dim: int, size: int) -> List[Tuple]:
    

    # e.g. if 2 dimension and size = 3
    # 1,1 : 3,3
    # 1,3 : 3,1
    # 3,1 : 1,3
    # 3,3 : 1,1

    # get a list of all corners that with 0 index in first dimension
    corners_all = it.product([0, size - 1], repeat = dim)
    corners_0 = [corner for corner in corners_all if corner[0] == 0]

    diagonals = []
    for corner in corners_0: 
        diagonal = []
        diagonal.append(corner) 
        # add rest of diagonal
        for i in range(1, size): 
            tmp = tuple(c - i for c in corner)
            inds = tuple(abs(t) for t in tmp)
            diagonal.append(inds)
        diagonals.append(diagonal)

    return diagonals


def lines_inds(dim: int, size: int, flatten: bool = True) -> \
               Tuple[Union[List[Tuple[int]], List[List[Tuple[int]]]], int]: 

    lines = []
    count = 0

    # loop over the numbers of dimensions in which the line exists
    for i in range(dim): 
        
        diagonals = diagonals_inds(i + 1, size)
        
        # loop over all possible combinations of i-dimensional hypercubes
        for j in it.combinations(range(dim), r = i + 1):
            for diagonal in diagonals:
                # the other dimensions can assume any position from a combination of all positions
                for position in it.product(range(size), repeat = dim - i - 1):
               
                    # these are the other dimension
                    od = set(range(dim)) - set(j)
                    
                    # for each cell in diagonal
                    diag_ext = []
                    for c in diagonal:
                        diag_ext.append(hp.insert_into_tuple(c, od, position))

                    lines.append(diag_ext)
                    #lines.extend(diag_ext) if flatten else lines.append(diag_ext)
    
    return lines, count


def get_lines_inds(lines: List[np.ndarray], dim: int) -> List[Tuple[Tuple[int]]]:

    # assume flat list of lines
    size = lines[0].size
    shape = [size] * dim

    lines_inds = []
    for line in lines:
        line_inds = []
        for j in range(size):
            cell_inds = np.unravel_index(line[j], shape)
            line_inds.append(cell_inds)
        lines_inds.append(tuple(line_inds))
    return lines_inds



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

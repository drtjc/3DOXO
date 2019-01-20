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
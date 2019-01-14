import numpy as np
import itertools as it
from pprint import pprint
from scipy.special import comb

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








size = 3
dim = 3

arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
#arr = np.zeros([size] * dim, int)




def lm(s, d):
    l = 0
    for i in range(1,d + 1):
        l += comb(d, i, True) * (s ** (d-i)) * (2 ** (i - 1)) 
    return l


def diagonals(arr): 
    diag = []
    
    def diagonal(arr):
        if arr.ndim == 1:
            diag.append(arr)
            return diag
        else:
            diagonal(arr.diagonal())
            diagonal(np.flip(arr, 0).diagonal())

    diagonal(arr)
    return diag    


def lines(arr, flatten = True):
    lines = []
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


arr[0,0,0] = 999
l = lines(arr)
pprint(l)
print(arr)
pprint(l)

#print(lm(size, dim))


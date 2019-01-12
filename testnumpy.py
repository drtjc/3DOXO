import numpy as np
from pprint import pprint
import itertools
from scipy.special import comb

def slice_planes(arr, axes, inds):
    sl = [slice(None)] * arr.ndim    
    try:
        for axis, ind in zip(axes, inds):
            sl[axis] = ind
    except:
        sl[axes] = inds
    return arr[tuple(sl)]

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s) + 1))


size = 9
dim = 3

arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
#arr = np.zeros([size] * dim, int)


def lm(s, d):
    l = 0
    for i in range(1,d + 1):
        l += comb(d, i, True) * (s ** (d-i)) * (2 ** (i - 1)) 
    return l

# sum of: num ways of selecting i dimensions x size ^ remaining dimension
#  * number of corners for (i-1)-cube i.e. side 

#print(list(powerset(range(dim))))
    
for i in range(dim): # i is how many dimensions the line is in
    for j in itertools.combinations(range(dim), r = i + 1):
        # for all dimensions that don't appear, they can take on all values
        diff = set(range(dim))  - set(j)
        pprint(diff)
        #  2 ** i lines to get for size ** (d - i) other inds
        # 

            


# print(lm(size, dim))

lines = []
# 1d
for axes in itertools.combinations(range(dim), dim - 1): 
    for inds in itertools.product(range(size), repeat = 2): 
        lines.append(slice_planes(arr, axes, inds))
# 2d
for axis in range(dim):
    for ind in range(size):
        lines.append(slice_planes(arr, axis, ind).diagonal())
        lines.append(np.flip(slice_planes(arr, axis, ind), 1).diagonal())
# 3d
lines.append(arr.diagonal().diagonal())
lines.append(np.flip(arr.diagonal(), 0).diagonal())
lines.append(np.flip(arr, (1, 2)).diagonal().diagonal())
lines.append(np.flip(np.flip(arr, (1, 2)).diagonal(), 0).diagonal())

# print(len(lines))
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



size = 9
dim = 3

arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
#arr = np.zeros([size] * dim, int)

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


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1))


# for each possible combination of all axes
# e.g. if 3 dimensions: (0), (1), (2), (0, 1), (0, 2), (1, 2), (0, 1, 2)
# print(list(powerset(range(dim))))
# s = list(powerset(range(dim)))
# print(s[1])

# we need all lines (cosecutive cells of length size) in every combination of axes.
# e.g. 1d line along (0), take other axes (1, 2) = size ^ 2 combinations. 
# For each combination line
# is got by adding 1, 2, ... size
# e.g. 2d line along (0,1): 2 possiblities x size (for other axes)
# e.g. 3d line 4 possibilites (if 4d axis then x4, if 5d axes then x 16)  


#t3 = itertools.product(range(size), repeat = dim)
#print(list(t3))


#pprint(lines)
#pprint(arr)
#pprint(np.flip(arr, (1, 2)))
#pprint(arr.diagonal())
print(len(lines))

# def lm(s, d):
#     l = 0
#     for i in range(1,d):
#         l += comb(d, i, True) * (s ** (d-i)) * i 
#     return l + ((2 ** dim) / 2) # corners

def lm(s, d):
    l = 0
    for i in range(1,d + 1):
        l += comb(d, i, True) * (s ** (d-i)) * (2 ** (i - 1)) 
    return l

# sum of: num ways of selecting i dimensions x size ^ remaining dimension
#  * number of corners for (i-1)-cube i.e. side 

for i in range(dim):
    pass
    # for each combination of i-axes out of d
        # for each combination of inds in remaining d - i axes
            


print(lm(size, dim))
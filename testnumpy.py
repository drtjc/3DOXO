import numpy as np
from pprint import pprint
import itertools

size = 4
dim = 3

arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
#arr = np.zeros([size] * dim, int)
#print(arr)

#s1 = arr[0,:,3]
#print(s1)

#np.fill_diagonal(arr, 99)
#print(arr)

#np.fill_diagonal(arr[0,:,:], 99)
#print(arr)

#np.fill_diagonal(arr[:,0,:], 99)
#print(arr)

def slice_planes(arr, axes, inds):
    sl = [slice(None)] * arr.ndim
    for axis, ind in zip(axes, inds):
        sl[axis] = ind
    return arr[tuple(sl)]

#print(arr[0,0,:])
#sl = slice_planes(arr, (0, 1), (0, 0))
#print(sl)
#arr[0,0,0] = 99
#print(sl)


#print(list(itertools.combinations(range(3), 2)))
arr[3,3,3] =999

lines = []
for axes in itertools.combinations(range(3), 2): 
    for inds in itertools.product(range(4), repeat = 2): 
        lines.append(slice_planes(arr, axes, inds))


pprint(lines)
pprint(arr)

## GETTING 2 PLANE DIAGONALS
#print(arr[0,:,:])
#print(np.flip(arr[0,:,:], 1))
#print(arr[0,:,:].diagonal())
#print(np.flip(arr[0,:,:], 1).diagonal())




#print(arr)
#print(arr.diagonal())

## GETTING 3 PLANE DIAGONALS
#print(arr.diagonal().diagonal())
#print(np.flip(arr.diagonal(), 0).diagonal())
#print(np.flip(arr, (1, 2)).diagonal().diagonal())
#print(np.flip(np.flip(arr, (1, 2)).diagonal(), 0).diagonal())

#arr[0,3,0] = 99
#l = []
#l.append(np.flip(np.flip(arr, (1, 2)).diagonal(), 0).diagonal())

#s1 = np.flip(np.flip(arr, (1, 2)).diagonal(), 0).diagonal()
#print(l[0])

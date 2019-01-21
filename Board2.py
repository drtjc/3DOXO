import numpy as np
import itertools as it
from scipy.special import comb
from collections import defaultdict
from typing import List, Callable, Union, Iterable, Tuple, Any, DefaultDict
from pprint import pprint

import hypercube as hc


class Board():

    def __init__(self, dim, size):
        self.dim = dim
        self.size = size
        self.arr = np.arange(size ** dim, dtype = int).reshape([size] * dim)
        self.num_lines = hc.num_lines(dim, size)
        self.lines, _ = hc.get_lines(self.arr)
        self.cells_lines = hc.get_cells_lines(self.lines, dim)
        self.clear()

    # should lines and cells_lines be generators??


    def clear(self):
        self.arr.fill(0)






if __name__ == "__main__":
 
    dim = 2
    size = 2
    board = Board(dim, size)

    #print(board.num_lines)
    print(board.cells_lines)
    #print(board.arr)
    #print(board.cells_lines)

    hk = ['W' + str(i) for i in range(1, size + 1)] + \
         ['S' + str(i) for i in range(2, size + 1)]

    hkf = frozenset(hk)
    print(hkf)
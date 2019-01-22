import numpy as np #type: ignore

from sys import getsizeof
from typing import NamedTuple
from pprint import pprint

import hypercube as hc




class Board():

    Memory = NamedTuple('Memory', [('arr', int), ('lines', int), ('cell_lines', int), ('total', int)]) 

    def __init__(self, d: int, n: int) -> None:
        try:
            self.d = d
            self.n = n
            self.arr = np.arange(n ** d, dtype = np.int64).reshape([n] * d)
            self.num_lines = hc.num_lines(d, n)
            self.lines, _ = hc.get_lines(self.arr)
            self.cells_lines = hc.get_cells_lines(self.lines, d)
            self.clear()
        except MemoryError:
            raise MemoryError("The board is too big to fit into available memory")


    # int64 supports integers from -2^63 to 2^63 - 1
    
    #size of arr = n ** d * 64 / 8 bytes
    # can use arr.nbytes    
    # should lines and cells_lines be generators??


    def clear(self):
        self.arr.fill(0)

    
    def memory(self) -> Memory:
        m = self.arr.nbytes, getsizeof(self.lines), getsizeof(self.cells_lines)
        return self.Memory(*m, sum(m))


if __name__ == "__main__":
 
    dim = 3
    size = 4
    board = Board(dim, size)

    print(board.num_lines)
    #print(board.cells_lines)
    #print(board.arr)
    #print(board.cells_lines)

    print(board.memory())

    hk = ['W' + str(i) for i in range(1, size + 1)] + \
         ['S' + str(i) for i in range(2, size + 1)]

    hkf = frozenset(hk)
    print(hkf)
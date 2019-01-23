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


from collections import abc
import numbers


class Game:

    def __init__(self, p1, p2): # settings incl. interactive
        self.p1 = p1
        self.p2 = p2
        self.moves = [] # record moves

    def move(self):
        pass
        # co-routine??

class Games(list):
    pass




class Cell:

    def __init__(self, position):
        self.position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        
        try:
            int(self.level)
            int(self.row)
            int(self.column)
        except:
            raise TypeError("position must be a integer sequence of length 3.")

        if any(int(val) not in range(1,5) for val in value):
            raise ValueError("position elements must be between 1 and 4 inclusive.") 

        self._position = tuple(int(val) for val in value)
        if len(self._position) != 3:
            raise ValueError("There must be 3 position elements.")
 
    @property
    def level(self):
        return self.position[0]

    @property
    def row(self):
        return self.position[1]

    @property
    def column(self):
        return self.position[2]

    @property
    def is_outer(self):
        # true if any position element is equal to 1 or 4
        return any(idx in [1, 4] for idx in self.position)

    @property
    def is_inner(self):
        # true if all position elements are equal to 2 or 3
        return not self.is_outer
    
    @property
    def is_outer_corner(self):
        # true if no position element is equal to 2
        return all(idx != 2 for idx in self.position)

    @property
    def is_outer_outer(self): # does not include corners
        if self.is_outer:
            # true if level = 1 or 4, row = 2 or 3, and column = 1 or 4
            return self.level in [1, 4] and self.row in [2, 3] \
                   and self.column in [1, 4]       
        else:
            return False

    @property
    def is_outer_inner(self):
        if self.is_outer:
            return not self.is_outer_corner and not self.is_outer_outer
        else:
            return False    
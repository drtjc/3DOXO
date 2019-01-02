import numbers
import itertools
from collections import UserDict

import Settings

class Board(UserDict):

    # think of rows, columns and levels as x, y and z planes (in 3d graph)
    LINES = {
        # lines on row plane
        'line_11c': ['111', '112', '113', '114'],
        'line_12c': ['121', '122', '123', '124'],
        'line_13c': ['131', '132', '133', '134'],
        'line_14c': ['141', '142', '143', '144'],
        'line_21c': ['211', '212', '213', '214'],
        'line_22c': ['221', '222', '223', '224'],
        'line_23c': ['231', '232', '233', '234'],
        'line_24c': ['241', '242', '243', '244'],
        'line_31c': ['311', '312', '313', '314'],
        'line_32c': ['321', '322', '323', '324'],
        'line_33c': ['331', '332', '333', '334'],
        'line_34c': ['341', '342', '343', '344'],
        'line_41c': ['411', '412', '413', '414'],
        'line_42c': ['421', '422', '423', '424'],
        'line_43c': ['431', '432', '433', '434'],
        'line_44c': ['441', '442', '443', '444'],
        # lines on column plane
        'line_1r1': ['111', '121', '131', '141'],
        'line_1r2': ['112', '122', '132', '142'],
        'line_1r3': ['113', '123', '133', '143'],
        'line_1r4': ['114', '124', '134', '144'],
        'line_2r1': ['211', '221', '231', '241'],
        'line_2r2': ['212', '222', '232', '242'],
        'line_2r3': ['213', '223', '233', '243'],
        'line_2r4': ['214', '224', '234', '244'],
        'line_3r1': ['311', '321', '331', '341'],
        'line_3r2': ['312', '322', '332', '342'],
        'line_3r3': ['313', '323', '333', '343'],
        'line_3r4': ['314', '324', '334', '344'],
        'line_4r1': ['411', '421', '431', '441'],
        'line_4r2': ['412', '422', '432', '442'],
        'line_4r3': ['413', '423', '433', '443'],
        'line_4r4': ['414', '424', '434', '444'],
        # lines on level plane
        'line_l11': ['111', '211', '311', '411'],
        'line_l12': ['112', '212', '312', '412'],
        'line_l13': ['113', '213', '313', '413'],
        'line_l14': ['114', '214', '314', '414'],
        'line_l21': ['121', '221', '321', '421'],
        'line_l22': ['122', '222', '322', '422'],
        'line_l23': ['123', '223', '323', '423'],
        'line_l24': ['124', '224', '324', '424'],
        'line_l31': ['131', '231', '331', '431'],
        'line_l32': ['132', '232', '332', '432'],
        'line_l33': ['133', '233', '333', '433'],
        'line_l34': ['134', '234', '334', '434'],
        'line_l41': ['141', '241', '341', '441'],
        'line_l42': ['142', '242', '342', '442'],
        'line_l43': ['143', '243', '343', '443'],
        'line_l44': ['144', '244', '344', '444'],
        # lines on row-column plane
        'line_1rc_1': ['111', '122', '133', '144'],
        'line_1rc_2': ['114', '123', '132', '141'],
        'line_2rc_1': ['211', '222', '233', '244'],
        'line_2rc_2': ['214', '223', '232', '241'],
        'line_3rc_1': ['311', '322', '333', '344'],
        'line_3rc_2': ['314', '323', '332', '341'],
        'line_4rc_1': ['411', '422', '433', '444'],
        'line_4rc_2': ['414', '423', '432', '441'],
        # lines on level-column plane
        'line_l1c_1': ['111', '212', '313', '414'],
        'line_l1c_2': ['114', '213', '312', '411'],
        'line_l2c_1': ['121', '222', '323', '424'],
        'line_l2c_2': ['124', '223', '322', '421'],
        'line_l3c_1': ['131', '232', '333', '434'],
        'line_l3c_2': ['134', '233', '332', '431'],
        'line_l4c_1': ['141', '242', '343', '444'],
        'line_l4c_2': ['144', '243', '342', '441'],
        # lines on level-row plane
        'line_lr1_1': ['111', '221', '331', '441'],
        'line_lr1_2': ['141', '231', '321', '411'],
        'line_lr2_1': ['112', '222', '332', '442'],
        'line_lr2_2': ['142', '232', '322', '412'],
        'line_lr3_1': ['113', '223', '333', '443'],
        'line_lr3_2': ['143', '233', '323', '413'],
        'line_lr4_1': ['114', '224', '334', '444'],
        'line_lr4_2': ['144', '234', '324', '414'],
        # lines on level-row-column plane
        'line_lrc_1': ['111', '222', '333', '444'],
        'line_lrc_2': ['114', '223', '332', '441'],
        'line_lrc_3': ['144', '233', '322', '411'],
        'line_lrc_4': ['141', '232', '323', '414']
    }

    def __init__(self):
        self.data = {}
        for l in range(1, 5):
            for r in range(1, 5):
                for c in range(1, 5):
                    position = str(l) + str(r) + str(c)
                    lines = {key: line for key, line in Board.LINES.items() 
                             if position in line}       
                    self[position] = Cell(position, lines)

    def clear(self):
        for position, _ in self.items():
            self[position].set_as_empty()


    def lines_info(self, position):
        lines_info = {}
        # lines_info to contain, by intersecting line:
        #   1. number of total cells with same value as position cell.
        #   2. max number of consecutive cells as position cell.
        #   3. If position cell is not empty, then if line contains 
        #      opposite (non-empty) value. If position cell is empty,
        #      then if line contains any non-empty values.  
        value = self[position].value
        for key, line in self[position].lines.items():
            line_values = [self[position].value == value for position in line]
            values_total = sum(line_values)
            values_consec = max(len(list(seq)) for value, seq in itertools.groupby(line_values) if value)

            lines_values_X = any([self[position].value == Cell.X for position in line])
            lines_values_O = any([self[position].value == Cell.O for position in line])
            if self[position].is_O:
                lines_values_opp = lines_values_X
            elif self[position].is_X:
                lines_values_opp = lines_values_O
            else: # empty
                lines_values_opp = lines_values_X or lines_values_O  
            
            lines_info[key] = [values_total, values_consec, lines_values_opp]
        return lines_info


class Cell:

    X = 'X'
    O = 'O'
    EMPTY = None

    def __init__(self, position, lines):
        self.position = position
        self.set_as_empty()
        self.lines = lines

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
    def value(self):
        return self._value

    @property
    def is_X(self):
        return self.value == Cell.X

    @property
    def is_O(self):
        return self.value == Cell.O

    @property
    def is_empty(self):
        return self.value == Cell.EMPTY

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
            return self.level in [1, 4] and self.row in [2, 3] and self.column in [1, 4]       
        else:
            return False

    @property
    def is_outer_inner(self):
        if self.is_outer:
            return not self.is_outer_corner and not self.is_outer_outer
        else:
            return False

    def set_as_X(self):
        self._value = Cell.X

    def set_as_O(self):
        self._value = Cell.O

    def set_as_empty(self):
        self._value = Cell.EMPTY



from pprint import pprint
   # def display_line        
if __name__ == "__main__":
    
    h1 = {'W4': 5000, 'S4': 1000, 'W3': 500, 'S3': 200, 'W2': 100, 'S2': 50, 'W1': 20, 'S1': 5}
    h2 = {'W4': 5000, 'S4': 1000, 'W3': 500, 'S3': 200, 'W2': 100, 'S2': 50, 'W1': 20, 'S1': 5}

    s1 = Settings.Settings(h1, 1)
    s2 = Settings.Settings(h1, 2)
    
    alls = Settings.AllSettings()
    alls['h1'] = h1
    alls['h2'] = h2

    print(alls['h1'])

    b = Board()
    b['111'].set_as_X()
    print(b['111'].value)
    
    b['112'].set_as_X()
    print(b['112'].value)

   # b['113'].set_as_O()
    print(b['113'].value)

    b['114'].set_as_X()
    print(b['114'].value)

    lv = b.lines_info('111')
    pprint(lv)

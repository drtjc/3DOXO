# from typing import List
# ADD TYPE ANNOTATIONS AT SOME POINT

class OXO_3D:

    def __init__(self, p1, p2):
        # p1 and p2 are expected to be Player classes
        # they should have different markers
        # they should have different names
        self.board = [[['_'] * 4 for i in range(4)] for i in range(4)]

    def __str__(self):
        return "3D OXO"

    def Move(self):
        self.board[0][1][2] = 'X' #plane, row, column

    def display(self):
        print(self.board)


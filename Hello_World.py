# from typing import List
# ADD TYPE ANNOTATIONS AT SOME POINT

class Player:

    def __init__(self, name, marker):
        self.name = name
        self.marker = marker
        
    @property
    def marker(self):
        return self.__marker

    @marker.setter
    def marker(self, value):
        self.__marker = value # check it is single character

    def __str__(self):
        return f'''Player's name is {self.name}. Marker is '{self.marker}\''''


    # add equality checks for Player



# rename to OXO_3D
class IIID_OXO:

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


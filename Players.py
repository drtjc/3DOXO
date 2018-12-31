# from typing import List
# ADD TYPE ANNOTATIONS AT SOME POINT

from collections import UserDict

class Player:

    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return f'''Player's name is {self.name}.'''

    # add equality checks for Player


class Players(UserDict):
    pass
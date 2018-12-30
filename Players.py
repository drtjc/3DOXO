# from typing import List
# ADD TYPE ANNOTATIONS AT SOME POINT

import collections

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


class Players(collections.UserDict):

    def __contains__(self, name): 
        return name in self.data

    def __setitem__(self, name, player): 
        self.data[name] = player


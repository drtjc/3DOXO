# from typing import List
# ADD TYPE ANNOTATIONS AT SOME POINT

from collections import UserDict

class Players(UserDict):
    
    def __init__(self):
        self.data = {}

    def __setitem__(self, name, player):
        if isinstance(player, Player):
            self.data[name] = player
        else:
            raise TypeError("Item must of type Player")



class Player:

    def __init__(self, name):
        self.name = name
        self.games = []
        
    def __str__(self):
        return f'''Player's name is {self.name}.'''

    








if __name__ == "__main__":
    pls = Players()
    p = Player('tom')
    pls[p.name] = p
    print(pls['tom'])

    q = Player('tom')
    pls[q.name] = q
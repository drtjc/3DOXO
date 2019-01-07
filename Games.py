from collections import UserList
from colorama import init, Fore, Back, Style
init()

import Board
import Players
import Settings

class Games():

    def __init__(self):
        self.games = []

 

class Game:

    OUTCOME = frozenset(['p1', 'p2', 'tie'])
    ADD_QUIT_GAMES = True

    def __init__(self, p1, p2, s1, s2):
        self.board = Board.Board()
        self.players = (p1, p2)
        self.settings = (s1, s2)
        self.moves = []
        self._was_quit = False
    
        ## check settings are of type Setting

    @property
    def was_quit(self):
        return self._was_quit
     
    def move(self):
        # determine which player is to play (indexed at 0); get corresponding settings   
        p = len(self.moves) % 2
        s = self.settings[p]
        if s.is_interactive:
            print("interactive")
            self.moves.append('111')
        else:
            print("heuristics")

        # if quit then self._was quit = TRUE
        
        
def underline(str):
    s = ""
    str2 =str#.replace(" ", chr(0x1680))
    #for ch in str:
    #    if ch.isspace():
    #        #s += "t\u0332"
    #        s = s + chr(0x00B7)
    #    else:
    #        s = s + ch + "\u0332"
    #return s

    return ''.join([chr + "\u0332" for chr in str2])
    #return ''.join([ch + chr(0x035F) for ch in str2])


def prRed(skk): print("\033[91m {}\033[00m" .format(skk)) 


if __name__ == "__main__":
    
    h1 = {'W4': 5000, 'S4': 1000, 'W3': 500, 'S3': 200, 'W2': 100, 'S2': 50, 'W1': 20}
    h2 = {'W4': 5000, 'S4': 1000, 'W3': 500, 'S3': 200, 'W2': 100, 'S2': 50, 'W1': 20}

    s1 = Settings.Setting(h1, 1)
    s2 = Settings.Setting(h1, 2)
    
    si1 = Settings.Setting.as_interactive()
    si2 = Settings.Setting.as_interactive()

    g = Game('tom', 'aviva', si1, s2)
    g.move()
    g.move()

    print('\033[31m' + underline("X") + "|" + underline("O") + "|" + "_" + "|" + underline("X") + "\n" + \
          underline("O") + "|" + underline("O") + "|" + "_" + "|" + "_" + "\n" + \
          "X" + "|" + "O" + "|" + " " + "|" + "X")

    print("X" + "\u20E4")
    print("X" + chr(0x20E4))

    print("\033[1;32;40m Bright Green  \n")

    print(Fore.RESET + Back.RESET + underline('testy test'))
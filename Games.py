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

    @staticmethod
    def underline(str):
        try:
            return ''.join([chr + "\u0332" for chr in str])
        except:
            return str

    def display_term(self, players = True, settings = True):
        print(self.underline("test"))
        vis = ""
        for cell in self.board.cells_rlc():
            
            #print(cell.position, end = ' ')

            if cell.is_empty:
                cell._value = "B"

            if not cell.is_front_face:
                #print("see")
                vis += self.underline(cell.value)
            else:
                #print("hi")
                vis += cell.value

            if not cell.is_right_face:
                #print("line")
                vis += "|"
            else:
                #print("here")
                if cell.is_bottom_face:
                    #print("bottom)")
                    vis += "\n"
                else:
                    vis += "  "
                    #print("space")    

        print(vis)
        return



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

    g.board[111].set_as_X()

    g.display_term()


    # print('\033[31m' + underline("X") + "|" + underline("O") + "|" + "_" + "|" + underline("X") + "\n" + \
    #       underline("O") + "|" + underline("O") + "|" + "_" + "|" + "_" + "\n" + \
    #       "X" + "|" + "O" + "|" + " " + "|" + "X")

    # print("X" + "\u20E4")
    # print("X" + chr(0x20E4))

    # print("\033[1;32;40m Bright Green  \n")

    # print(Fore.RESET + Back.RESET + underline('testy test'))
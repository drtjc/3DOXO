class Settings:

    def __init__(self, *, interactive = False, Win = 0, StopLoss = 0): #what about a dictionary argument
        self.interactive = interactive
        self.settings = {'Win': Win, 'StopLoss': StopLoss}
        
    @classmethod
    def play_interactive(cls):
        return cls(interactive = True)

    @classmethod
    def play_heuristics(cls, *, Win, StopLoss):
        return cls(Win = Win, StopLoss = StopLoss)

    
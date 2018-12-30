from collections import abc

class Settings:

    HEURISITC_KEYS = {'W4', 'W3', 'W2', 'W1', 'S4', 'S3', 'S2', 'S1'}
    MAX_DEPTH = 5

    def __init__(self, heuristics = None, depth = None): 
        self.heuristics = heuristics
        self.depth = depth
        
    @classmethod
    def as_interactive(cls):
        return cls()

    @classmethod
    def as_heuristics(cls, heuristics, depth):
        return cls(heuristics, depth)

    @property
    def heuristics(self):
        return self._heuristics

    @heuristics.setter
    def heuristics(self, value):
        # check that value is a dictionary
        if isinstance(value, abc.Mapping):
            # value is a dictionary - check that the right keys exist
            if value.keys() == Settings.HEURISITC_KEYS:
                self._heuristics = value
            else:
                missing_keys = Settings.HEURISITC_KEYS - value.keys()
                extra_keys = value.keys() - Settings.HEURISITC_KEYS           
                msg = f'''Heuristic keys are not same. Missing keys 
                          are {missing_keys}. Extra keys are {extra_keys}'''
                raise ValueError(msg)
        else:
            raise TypeError("value should be a mapping (dictionary)")

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        self._depth = max(1, min(value, Settings.MAX_DEPTH))

    @property
    def is_interactive(self):
        if self.heuristics is None: 
            return True
        else:
            return False

    @property
    def is_heuristics(self):
        return not self.is_interactive


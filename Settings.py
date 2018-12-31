from collections import abc
import numbers

hk = {'W4': 5000, 'S4': 1000, 'W3': 500, 'S3': 200, 'W2': 100, 'S2': 50, 'W1': 20, 'S1': 5}
hk_bad = {'W4': 5000, 'S4': 1000, 'W3': 500, 'S3': 200, 'W2': 100, 'S2': 50, 'W1': 20, 'S1': 'test'}

class Settings:

    HEURISITC_KEYS = frozenset(['W4', 'W3', 'W2', 'W1', 'S4', 'S3', 'S2', 'S1'])
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
        # check that heuristics is a dictionary
        if isinstance(value, abc.Mapping):
            # check that heuristics has the right keys
            if value.keys() == Settings.HEURISITC_KEYS:
                # check that heuristics has numeric values
                if all(isinstance(val, numbers.Real) for val in value.values()):
                    self._heuristics = value
                else:
                    non_numeric_keys = {key for key, val in value.items() \
                                        if not isinstance(val, numbers.Real)}
                    msg = f'All heuristics values must be numeric. Keys ' \
                          f'with non-numeric values are {non_numeric_keys}.'
                    raise TypeError(msg)
            else:
                missing_keys = Settings.HEURISITC_KEYS - value.keys()
                extra_keys = value.keys() - Settings.HEURISITC_KEYS           
                msg = f'heuristics keys are not same. Missing keys ' \
                      f'are {missing_keys}. Extra keys are {extra_keys}.'
                raise ValueError(msg)
        else:
            raise TypeError("heuristics should be a mapping (dictionary).")

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value):
        if isinstance(value, numbers.Integral):
            if value >= 1 and value <= Settings.MAX_DEPTH:
                self._depth = value
            else:
                msg = f'depth must be between 1 and {Settings.MAX_DEPTH} ' \
                      f'inclusively.'
                raise ValueError(msg)
        else:
            raise TypeError("depth must be an integer.")

    @property
    def is_interactive(self):
        if self.heuristics is None: 
            return True
        else:
            return False

    @property
    def is_heuristics(self):
        return not self.is_interactive


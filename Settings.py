import numbers
from collections import abc
from collections import UserDict

class Settings(UserDict):
    
    def __init__(self):
        self.data = {}

    def __setitem__(self, name, setting):
        if isinstance(setting, Setting):
            self.data[name] = setting
        else:
            raise TypeError("Item must of type Setting")    


class Setting:

    HEURISITC_KEYS = frozenset(['W4', 'W3', 'W2', 'W1', 'S4', 'S3', 'S2'])
    MAX_DEPTH = 5

    def __init__(self, heuristics = None, depth = None): 
        self.heuristics = heuristics
        self.depth = depth

    def __repr__(self):
        if self.is_interactive:
            s = "Interactive"
        else:
            s = "D=" + str(Setting.MAX_DEPTH) + ":"
            for key, value in self.heuristics.items():
                s += ":" + key + "=" + str(value)
        return s

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
        if value is None:
            self._heuristics = None
            return

        # check that heuristics is a dictionary
        if isinstance(value, abc.Mapping):
            # check that heuristics has the right keys
            if value.keys() == Setting.HEURISITC_KEYS:
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
                missing_keys = Setting.HEURISITC_KEYS - value.keys()
                extra_keys = value.keys() - Setting.HEURISITC_KEYS           
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
        if value is None:
            self._depth = None
            return

        if isinstance(value, numbers.Integral):
            if value >= 1 and value <= Setting.MAX_DEPTH:
                self._depth = value
            else:
                msg = f'depth must be between 1 and {Setting.MAX_DEPTH} ' \
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


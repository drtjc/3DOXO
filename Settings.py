import numbers
from collections import abc

from typing import Generic, Dict, Optional, Type, TypeVar
T = TypeVar('T', bound = 'Settings')

class Settings:

    def __init__(self, interactive: bool, n: Optional[int], heuristics: Optional[Dict[str, int]], 
                 depth: Optional[int]) -> None: 
        
        self.interactive = interactive
        self.n = n

        self.heuristics = heuristics
        self.HEURISTIC_KEYS = None
        if heuristics is not None:
            self.HEURISTIC_KEYS = frozenset(['W' + str(i) for i in range(1, n + 1)] + \
                                            ['S' + str(i) for i in range(2, n + 1)])
        self.depth = depth

    def __repr__(self) -> str:
        if self.interactive:
            s = "Interactive"
        else:
            s = "D=" + str(self.depth) + ":"
            for key, value in self.heuristics.items():
                s += ":" + key + "=" + str(value)
        return s

    @classmethod
    def as_interactive(cls: Type[T]) -> T:
        return cls(True, None, None, None)

    @classmethod
    def as_heuristics(cls: Type[T], n: int, heuristics: Optional[Dict[str, int]] = None, 
                      depth: Optional[int] = 1) -> T:
        return cls(False, n, heuristics, depth)

    @property
    def heuristics(self) -> Optional[Dict[str, int]]:
        return self._heuristics

    @heuristics.setter
    def heuristics(self, value: Optional[Dict[str, int]]) -> None:
        if self.interactive:
            self._heuristics = None
            return

        # if interactive but no heuristics then build default ones of form
        # W1 = 1, S2 = 2, W2 = 4, S3 = 8, W3 = 16, ..., Si = 2^(2i-3), Wi = 2^(2i-2), ...
        if value is None:
            self._heuristics = {**{'W' + str(i): 2 ** (2 * i - 2) for i in range(1, self.n + 1)},
                                **{'S' + str(i): 2 ** (2 * i - 3) for i in range(2, self.n + 1)}}
            return

        # check user-defined heuristics are valid
        # check that heuristics is a dictionary
        if isinstance(value, abc.Mapping):
            # check that heuristics has the right keys
            if value.keys() == self.HEURISTIC_KEYS:
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
                missing_keys = self.HEURISTIC_KEYS - value.keys()
                extra_keys = value.keys() - self.HEURISTIC_KEYS           
                msg = f'heuristics keys are incorrect. Missing keys ' \
                      f'are {missing_keys}. Extra keys are {extra_keys}.'
                raise ValueError(msg)
        else:
            raise TypeError("heuristics should be a mapping (dictionary).")




if __name__ == "__main__":

    s = Settings.as_heuristics(6)
    print(s.heuristics)

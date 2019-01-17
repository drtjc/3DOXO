from typing import Sequence, Union, Iterable

def sadd(s: str) -> str:
    t : Sequence[int] = (1, 2)
    print(s + s)
    return "v"


def itt(i: Union[int, Iterable[int]]):
    print(i)
    return None


if __name__ == "__main__":
    sadd("1")

    for i in range(5):
        print(i)

    itt(range(5))
    itt([1,2,3])

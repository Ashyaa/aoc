#!/usr/bin/env python3

import contextlib

from pathlib import Path
from AoC.util import show


CWD = Path(__file__).parent


INPUT = (2947, 3029)


get_index = lambda x, y: 1+sum(t for t in range(x)) + sum(t for t in range(x+1, x+y))


def compute_code(index: int) -> int:
    res = 20151125
    for _ in range(index-1):
        res = (res * 252533) % 33554393
    return res

@show
def first() -> int:
    return compute_code(get_index(*INPUT))


@show
def second() -> None:
    pass


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert get_index(4, 3) == 18
        assert get_index(1, 6) == 21
        assert get_index(3, 2) == 8
        assert compute_code(1) == 20151125
        assert compute_code(2) == 31916031
        assert compute_code(21) == 33511524


test_example()
first() # 19980801
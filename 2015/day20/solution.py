#!/usr/bin/env python3

import contextlib

from math import sqrt
from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent
INPUT = 33100000


def divisors(n: int) -> List[int]:
    res = [1]
    for i in range(2, int(sqrt(n))+1):
        if n%i == 0:
            res.extend([i, n//i])
    return res + [n]


@show
def first() -> int:
    s = INPUT // 10
    for i in range(s):
        if sum(divisors(i)) >= s:
            return i


@show
def second() -> int:
    for i in range(INPUT):
        divs = [d for d in divisors(i) if i <= d*50]
        if 11 * sum(divs) >= INPUT:
            return i


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert sum(divisors(827500)) == 1815044


test_example()
first() # 776160
second() # 786240
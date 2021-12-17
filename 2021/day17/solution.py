#!/usr/bin/env python3

import contextlib
from math import sqrt
from pathlib import Path
from typing import *

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Tuple[int, int, int, int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        x, y = reader.readline().strip()[13:].split(", ")
        x1, x2 = x[2:].split("..")
        y1, y2 = y[2:].split("..")
        return int(x1), int(x2), int(y1), int(y2)


T = lambda n: (n*(n+1))//2
DX = lambda x, n: (x*n - T(n-1)) if x >= n else (x*x - T(x-1))
DY = lambda y, n: y*n - T(n-1)


def reaches(x: int, x1: int, x2: int, max_step: int) -> List[int]:
    return [i for i in range(1, max_step+1) if x1 <= DX(x, i) <= x2]


distance = lambda x, y: round(sqrt(x*x + y*y))

@show
def first(inp) -> Tuple[int, int]:
    res, x = [], 1
    visited = set()
    dist = distance(inp[1], inp[2])
    while T(x) < inp[0]:
        x += 1
    while x <= inp[1]:
        steps = reaches(x, inp[0], inp[1], dist)
        for i in steps:
            for y in range(inp[2]-1, i+1):
                if inp[2] <= DY(y, i) <= inp[3]:
                    visited.add((x,y))
                    res.append(DY(y,y) if y > 0 else 0)
        x += 1
    return max(res), len(visited)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == (45, 112)


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 4753, 1546

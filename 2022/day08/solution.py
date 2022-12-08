#!/usr/bin/env python3

import contextlib
from functools import reduce
from itertools import product
from pathlib import Path
from typing import List, Tuple

from AoC.util import show

CWD = Path(__file__).parent
LENGTH, WIDTH = -1, -1


def read_input(filename: str = "input.txt") -> List[List[int]]:
    global LENGTH, WIDTH
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        lines = reader.read().split("\n")
        LENGTH, WIDTH = len(lines), len(lines[0])
        return [[int(c) for c in l] for l in lines]


def axes(grid: List[List[int]], x: int, y: int) -> List[List[int]]:
    return [
      list(reversed([l[y] for l in grid[0:x]])),
      [l[y] for l in grid[x+1:LENGTH]],
      list(reversed(grid[x][0:y])),
      grid[x][y+1:WIDTH],
    ]


def process(grid: List[List[int]], x: int, y: int) -> Tuple[bool, int]:
    if x == 0 or x == LENGTH-1 or y == 0 or y == WIDTH-1:
       return True, 0
    f1 = lambda ax : max(ax) < grid[x][y]
    def f2(ax: List[int]) -> int:
        res = 0
        for n in ax:
            res += 1
            if n >= grid[x][y]:
                break
        return res
    axs = axes(grid, x, y)
    return any(map(f1, axs)), reduce(lambda x, y : x*y, map(f2, axs))


@show
def run(grid: List[List[int]]) -> int:
    data = [process(grid, x, y) for x, y in product(range(LENGTH), range(WIDTH))]
    return sum(d[0] for d in data),  max(d[1] for d in data)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        res  = run(read_input("example.txt"))
        assert res == (21, 8), res


test_example()
run(read_input()) # 1798, 259308
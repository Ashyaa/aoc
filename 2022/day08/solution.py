#!/usr/bin/env python3

import contextlib

from itertools import product
from pathlib import Path
from typing import List, Dict
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[List[int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return [[int(c) for c in l] for l in reader.read().split("\n")]


def visible(grid: List[List[int]], x: int, y: int) -> bool:
    length = len(grid)
    width = len(grid[0])
    if x == 0 or x == length or y == 0 or y == width:
       return True
    tree = grid[x][y]
    axis_1 = [l[y] for l in grid[0:x+1]]
    axis_2 = [l[y] for l in grid[x:length]]
    axis_3 = grid[x][0:y+1]
    axis_4 = grid[x][y:width]
    f = lambda ax : tree == max(ax) and ax.count(tree) == 1
    return f(axis_1) or f(axis_2) or f(axis_3) or f(axis_4)


def score(grid: List[List[int]], x: int, y: int) -> int:
    length = len(grid)
    width = len(grid[0])
    if x == 0 or x == length or y == 0 or y == width:
       return 0
    tree = grid[x][y]
    axis_1 = reversed([l[y] for l in grid[0:x]])
    axis_2 = [l[y] for l in grid[x+1:length]]
    axis_3 = reversed(grid[x][0:y])
    axis_4 = grid[x][y+1:width]
    def f(ax: List[int]) -> int:
        res = 0
        for n in ax:
            res += 1
            if n >= tree:
                break
        return res
    return f(axis_1) * f(axis_2) * f(axis_3) * f(axis_4)


@show
def first(grid: List[List[int]]) -> int:
    length = len(grid)
    width = len(grid[0])
    return sum(visible(grid, x, y) for x, y in product(range(length), range(width)))


@show
def second(grid: List[List[int]]) -> int:
    length = len(grid)
    width = len(grid[0])
    return max(score(grid, x, y) for x, y in product(range(length), range(width)))


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        r1  = first(inp)
        assert r1 == 21, r1
        r2  = second(inp)
        assert r2 == 8, r2


test_example()
s = read_input()
first(s)  # 2061777
second(s)  # 4473403

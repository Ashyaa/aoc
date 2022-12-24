#!/usr/bin/env python3

import contextlib
from functools import cache
from heapq import heappop, heappush
from pathlib import Path
from typing import FrozenSet, Tuple

from AoC.util import show

CWD = Path(__file__).parent
START = (-1,0)
WINDS = {
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1),
    "^": (-1,0),
    '.': (0, 0)
}
T_WIND = Tuple[Tuple[int,int], Tuple[int,int]]


def read_input(filename: str = "input.txt") -> Tuple[FrozenSet[Tuple[int,int]], FrozenSet[T_WIND], int, int]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        lines = reader.read().splitlines()[1:-1]
        height = len(lines)
        width = len(lines[0]) - 2
        grid, winds = set(), set()
        for x, row in enumerate(lines):
            for y, c in enumerate(row[1:-1]):
                grid.add((x, y))
                if c != '.': winds.add(((x, y), WINDS[c]))
        grid.add(START)
        grid.add((height, width-1))
        grid, winds = frozenset(grid), frozenset(winds)
        return grid, winds, height, width


@cache
def update(grid: FrozenSet[Tuple[int,int]], winds: FrozenSet[T_WIND],
         height: int, width: int) -> Tuple[FrozenSet[T_WIND],FrozenSet[Tuple[int,int]]]:
    winds = frozenset((((x+dx)%height, (y+dy)%width), (dx, dy)) for (x, y), (dx, dy) in winds)
    free = grid - {b[0] for b in winds}
    return winds, free


def dist(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2-x1) + abs(y2-y1)


def walk(start: Tuple[int, int], goal: Tuple[int, int], grid: FrozenSet[Tuple[int,int]],
         winds: FrozenSet[T_WIND], height: int, width: int) -> Tuple[int, FrozenSet[T_WIND]]:
    stack, seen, step = [], set(), 0
    heappush(stack, (0, start, winds, step))
    while stack:
        _, (x, y), cur_winds, t = heappop(stack)
        cur_winds, free = update(grid, cur_winds, height, width)
        for (dx, dy) in WINDS.values():
            p = (x+dx, y+dy)
            if p == goal:
                return t+1, cur_winds
            elif p in free:
                if (p, cur_winds) not in seen:
                    seen.add((p, cur_winds))
                    heappush(stack, (dist(*p, *goal)+t, p, cur_winds, t+1))
    return -1, frozenset()


@show
def first(grid: FrozenSet[Tuple[int,int]], winds: FrozenSet[T_WIND], height: int, width: int) -> int:
    return walk(START, (height, width-1), grid, winds, height, width)[0]


@show
def second(grid: FrozenSet[Tuple[int,int]], winds: FrozenSet[T_WIND], height: int, width: int) -> int:
    end = (height, width-1)
    r1 = walk(START, end, grid, winds, height, width)
    r2 = walk(end, START, grid, r1[1], height, width)
    r3 = walk(START, end, grid, r2[1], height, width)
    return r1[0] + r2[0] + r3[0]


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(*inp)
        assert r1 == 18, r1
        r2  = second(*inp)
        assert r2 == 54, r2


test_example()
s = read_input()
first(*s)  # 238
second(*s)  # 751

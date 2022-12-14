#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import Set, Tuple
from AoC.util import show


CWD = Path(__file__).parent

ITEMS = ["A","B","C"]
PLAYS = ["X","Y","Z"]


def read_input(filename: str = "input.txt") -> Set[Tuple[int, int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = set()
        for l in reader.readlines():
            tmp = [eval(c) for c in l.strip().split(" -> ")]
            for i, _ in enumerate(tmp[:-1]):
                step_x = 1 if tmp[i][0] <= tmp[i+1][0] else -1
                step_y = 1 if tmp[i][1] <= tmp[i+1][1] else -1
                res.update(
                    [(x, y)
                        for x in range(tmp[i][0], tmp[i+1][0]+step_x, step_x)
                        for y in range(tmp[i][1], tmp[i+1][1]+step_y, step_y)
                ])
    return res


def sand(s: Set[Tuple[int, int]], max: int) -> Tuple[int, int]:
    res = (500, 0)
    while res[1] <= max:
        x, y = res
        new_y = y+1
        if (x, new_y) not in s:
            res = (x, new_y)
            continue
        if (x-1, new_y) not in s:
            res = (x-1, new_y)
            continue
        if (x+1, new_y) not in s:
            res = (x+1, new_y)
            continue
        break
    return res


@show
def run(s: Set[Tuple[int, int]], p2: bool = False) -> int:
    abyss = max(c[1] for c in s)
    count = 0
    cond = lambda c: c == (500,0) if p2 else c[1] >= abyss
    while True:
        c = sand(s, abyss)
        if cond(c):
            break
        count += 1
        s.add(c)
    return count + 1 if p2 else count


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        r1  = run(inp.copy())
        assert r1 == 24, r1
        r2  = run(inp.copy(), True)
        assert r2 == 93, r2


test_example()
s = read_input()
run(s.copy())  # 1001
run(s.copy(), True)  # 27976

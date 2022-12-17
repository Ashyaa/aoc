#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Set, Tuple
from AoC.util import show


CWD = Path(__file__).parent
ROCKS: List[List[Tuple[int,int]]] = [
    [(i, 0) for i in range(4)],
    [(i, 1) for i in range(3)] + [(1, 0), (1, 2)],
    [(i, 0) for i in range(3)] + [(2, 1), (2, 2)],
    [(0, i) for i in range(4)],
    [(i, j) for i in range(2) for j in range(2)],
]


def read_input(filename: str = "input.txt") -> str:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return reader.read().strip()


def drop(i: int, dropped: Set[Tuple[int,int]], height: int, gas: int, gases: str) -> Tuple[Set[Tuple[int,int]], int]:
    rock = ROCKS[i%len(ROCKS)]
    width = max(r[0] for r in rock)
    x, y = 2, height + 4
    while True:
        dx = 0
        if gases[gas% len(gases)] == "<" and x > 0:
            dx = -1
        elif gases[gas% len(gases)] == ">" and x + width < 6:
            dx = 1
        if dx != 0 and any((x+dx+rx,y+ry) in dropped for rx,ry in rock):
            dx = 0
        x += dx
        gas = (gas  + 1)
        if y == 1 or any((x+rx,y-1+ry) in dropped for rx,ry in rock):
            break
        y -= 1
    return dropped.union({(x+rx,y+ry) for rx, ry in rock}), gas


def find_period(arr: List[int]) -> Tuple[int, int]:
    s = "".join(map(str, reversed(arr)))
    ln, sp = len(s), 20
    period = s[sp+1:].index(s[:sp]) + sp + 1
    begin = 0
    while True:
        if s[ln-sp-begin:ln-begin] == s[ln-sp-begin-period:ln-begin-period]: break
        begin += 1
    return begin, period


@show
def run(gases: str) -> Tuple[int, int]:
    nb_rocks, gas, height = 0, 0, 0
    dropped = set()
    sample = []
    while nb_rocks < 2000:
        dropped, gas = drop(nb_rocks, dropped, height, gas, gases)
        nb_rocks += 1
        new_height = max(d[1] for d in dropped)
        sample.append(new_height- height)
        height = new_height
    b, p = find_period(sample)
    f1 = lambda n: ((n - b + 1) // p, (n - b + 1) % p)
    f2  = lambda f, r: sum(sample[:b])+ (f * sum(sample[b:b+p])) + sum(sample[b:b+r-1])
    return f2(*f1(2022)), f2(*f1(1000000000000))


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = run(inp)
        assert r1 == (3068, 1514285714288), r1


test_example()
s = read_input()
run(s)  # 3232, 1585632183915

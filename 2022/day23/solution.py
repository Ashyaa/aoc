#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import Iterable, List, Dict, Set,Tuple
from AoC.util import show


CWD = Path(__file__).parent

DELTAS = [-1,0,1]
RULES = [
    (-1, 0), # N
    (1, 0),  # S
    (0, -1), # W
    (0, 1),  # E
]


def read_input(filename: str = "input.txt") -> Set[Tuple[int,int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = set()
        for i, l in enumerate(reader.read().splitlines()):
            for j, c in enumerate(l):
                if c == "#":
                    res.add((i,j))
        return res


def propose(x: int, y: int, r: int, l: Set[Tuple[int,int]]) -> Tuple[int, int]:
    neighbours = sum((x+dx, y+dy) in l for dx in DELTAS for dy in DELTAS)
    if neighbours == 1:
        return x,y
    for i in range(4):
        r_idx = (r + i) % 4
        rx, ry = RULES[r_idx]
        if rx == 0:
            check = set([(x+dx, y+ry) for dx in DELTAS])
        else:
            check = set([(x+rx, y+dy) for dy in DELTAS])
        if l.isdisjoint(check):
            return x+rx, y+ry
    return x,y


def run(elves: Set[Tuple[int,int]], r: int) -> Set[Tuple[int,int]]:
    proposals = {}
    for elf in elves:
        p = propose(*elf, r, elves)
        if p == elf:
            continue
        proposals[elf] = p
    prop_list = list(proposals.values())
    unique = {p: prop_list.count(p) == 1 for p in prop_list}
    res = set()
    for elf in elves:
        if elf not in proposals:
            res.add(elf)
            continue
        prop = proposals[elf]
        if unique[prop]:
            res.add(prop)
        else:
            res.add(elf)
    return res


@show
def first(l: Set[Tuple[int,int]]) -> int:
    elves = l.copy()
    r = 0
    for _ in range(10):
        elves = run(elves, r)
        r = (r + 1) % 4
    x_axis = [x for x, _ in elves]
    y_axis = [y for _, y in elves]
    return (max(x_axis)-min(x_axis)+1) * (max(y_axis)-min(y_axis)+1) - len(elves)


@show
def second(l: Set[Tuple[int,int]]) -> int:
    elves = l.copy()
    r = 0
    i = 0
    while True:
        i += 1
        new_elves = run(elves, r)
        if elves == new_elves:
            return i
        elves = new_elves
        r = (r + 1) % 4


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 110, r1
        r2  = second(inp)
        assert r2 == 20, r2


test_example()
s = read_input()
first(s)  # 4068
second(s)  # 968

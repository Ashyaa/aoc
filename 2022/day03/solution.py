#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent


priority = lambda c: ord(c) -96 if c.islower() else ord(c) - 38


def read_input(filename: str = "input.txt") -> List[str]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return [l.strip() for l in reader.readlines()]


def sack_prio(s: str) -> int:
    p1, p2 = set(s[int(len(s)/2):]), set(s[:int(len(s)/2)])
    return priority(p1.intersection(p2).pop())


def group_prio(l: List[str]) -> int:
    r = list(map(set, l))
    return priority(r[0].intersection(*r[1:]).pop())


@show
def first(l: List[str]) -> int:
    return sum(sack_prio(rs) for rs in l)


@show
def second(l: List[str]) -> int:
    return sum(group_prio(l[i:i+3]) for i in range(0, len(l), 3))


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 157, r1
        r2  = second(inp)
        assert r2 == 70, r2


test_example()
s = read_input()
first(s)  # 7746
second(s)  # 2604

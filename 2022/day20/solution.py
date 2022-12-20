#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent
KEY = 811589153


def read_input(filename: str = "input.txt") -> List[Tuple[int,int]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return [(i,int(l)) for i, l in enumerate(reader.read().splitlines())]


def mix(l: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
    size = len(l)
    for o in range(size):
        idx, order, n = next((idx, order, n) for idx, (order, n) in enumerate(l) if order == o)
        left, right = l[:idx], l[idx+1:]
        l = left + right
        new_idx = idx + n
        if new_idx <= 0 or new_idx >= size:
            new_idx = new_idx % (size - 1)
        l.insert(new_idx, (order, n))
    return l


@show
def first(l: List[Tuple[int,int]]) -> int:
    l = mix(l)
    zero_idx = next(i for i, (_, n) in enumerate(l) if n == 0)
    return sum(l[(zero_idx + i * 1000) % len(l)][1] for i in range(1,4))


@show
def second(l: List[Tuple[int,int]]) -> int:
    l = [(o, n * KEY) for (o, n) in l]
    for _ in range(10):
        l = mix(l)
    zero_idx = next(i for i, (_, n) in enumerate(l) if n == 0)
    return sum(l[(zero_idx + i * 1000) % len(l)][1] for i in range(1,4))


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp.copy())
        assert r1 == 3, r1
        r2  = second(inp)
        assert r2 == 1623178306, r2


test_example()
s = read_input()
first(s)  # 7713
second(s)  # 1664569352803

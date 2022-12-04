#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[set[int], set[int]]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        res = []
        for l in reader.readlines():
            int_list = list(map(int, l.strip().replace(",", "-").split('-')))
            range_1, range_2 = range(int_list[0], int_list[1]+1), range(int_list[2], int_list[3]+1)
            res.append((set(range_1), set(range_2)))
        return res


@show
def first(l: List[Tuple[set[int], set[int]]]) -> int:
    return sum(len(a.intersection(b)) == min(len(a), len(b)) for a, b in l)


@show
def second(l: List[Tuple[set[int], set[int]]]) -> int:
    return sum(len(a.intersection(b)) != 0 for a, b in l)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 2, r1
        r2  = second(inp)
        assert r2 == 4, r2


test_example()
s = read_input()
first(s)  # 576
second(s)  # 905

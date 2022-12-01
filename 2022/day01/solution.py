#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[List[int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        tmp, res = [], []
        for l in reader.readlines():
            if l.strip() != "":
                tmp.append(int(l))
            else:
                res.append(tmp)
                tmp = []
        if tmp:
            res.append(tmp)
    return res



@show
def first(l: List[List[int]]) -> int:
    return max(sum(sl) for sl in l)


@show
def second(l: List[List[int]]) -> int:
    return sum(n for n in sorted([sum(sl) for sl in l])[-3:])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 24000, r1
        r2  = second(inp)
        assert r2 == 45000, r2


test_example()
s = read_input()
first(s)  # 68292
second(s)  # 203203

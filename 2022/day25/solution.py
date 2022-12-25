#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent
MAP = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}
SNAF = ["0", "1", "2", "1=", "1-", "10"]


def read_input(filename: str = "input.txt") -> List[str]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return reader.read().splitlines()


def to_decimal(s: str) -> int:
    res, i = 0, 0
    for c in reversed(s):
        res += (MAP[c] * pow(5, i))
        i += 1
    return res


def to_snafu(n: int) -> str:
    s, i = "", 0
    while n:
        m = n%5
        if len(s) > i:
            s = SNAF[m+1] + s[1:]
        else:
            s = SNAF[m] + s
        n //= 5
        i += 1
    return s


@show
def first(l: List[str]) -> str:
    return to_snafu(sum(to_decimal(s) for s in l))


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == "2=-1=0", r1


test_example()
s = read_input()
first(s)  # 2=01-0-2-0=-0==-1=01

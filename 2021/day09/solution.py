#!/usr/bin/env python3

import contextlib

from functools import reduce
from pathlib import Path

from typing import *
from AoC.util import show

import numpy as np


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> np.ndarray:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        arr = []
        lines = reader.readlines()
        for l in lines:
            line_len = len(l.strip())
            for c in l.strip():
                arr.append(int(c))
        return np.array(arr).reshape(len(lines), line_len)


def low_points(inp: np.ndarray) -> List[Tuple[int, int]]:
    res = []
    for (x,y), item in np.ndenumerate(inp):
        arr = np.append(inp[max(0,x-1):x+2,y].flatten(), (inp[x, max(0,y-1):y+2].flatten()))
        if min(arr) == item and np.count_nonzero(arr == item) == 2:
            res.append((x,y))
    return res


@show
def first(inp: np.ndarray) -> int:
    return sum(inp[x,y]+1 for x,y in low_points(inp))


def basin(inp: np.ndarray, x: int, y: int) -> int:
    inp[x,y] = 100
    def rec(x2, y2) -> int:
        if x2 < 0 or y2 < 0:
              return 0
        with contextlib.suppress(IndexError):
            neighbor = inp[x2,y2]
            if neighbor < 9:
                return basin(inp, x2, y2)
        return 0
    return 1 + rec(x-1,y) + rec(x+1,y) + rec(x,y-1) + rec(x,y+1)


@show
def second(inp: np.ndarray) -> int:
    sizes = [basin(inp, x, y) for x, y in low_points(inp)]
    return reduce(lambda x, y: x*y, sorted(sizes)[-3:])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 15
        assert second(inp) == 1134


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 506
    second(inp)  # 931200

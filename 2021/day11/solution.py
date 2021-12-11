#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import *

import numpy as np
from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> np.ndarray:
    input_file = CWD.joinpath(filename)
    return np.genfromtxt(input_file, dtype=int, delimiter=1)


def flash(inp: np.ndarray) -> int:
    res = set()
    q = [(x,y) for (x,y), item in np.ndenumerate(inp) if item > 9]
    while q:
        x, y = q.pop()
        res.add((x,y))
        inp[max(0,x-1):x+2,max(0,y-1):y+2] += 1
        q = [(x,y) for (x,y), item in np.ndenumerate(inp) if item > 9 and (x,y) not in res]
    return len(res)


@show
def first(inp: np.ndarray, steps: int = 100) -> int:
    res = 0
    for _ in range(steps):
        inp += 1
        res += flash(inp)
        inp = np.where(inp>9, 0,inp)
    return res


@show
def second(inp: np.ndarray) -> int:
    count = 0
    while True:
        count += 1
        inp += 1
        if flash(inp) == 100:
            return count
        inp = np.where(inp>9, 0,inp)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first(read_input("example.txt"), 10) == 204
        assert first(read_input("example.txt")) == 1656
        assert second(read_input("example.txt")) == 195


if __name__ == "__main__":
    test_example()
    first(read_input())  # 1673
    second(read_input())  # 279

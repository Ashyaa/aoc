#!/usr/bin/env python3

import contextlib
from functools import reduce
from pathlib import Path
from typing import *

import numpy as np
from AoC.util import show
from scipy.ndimage import generic_filter

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> np.ndarray:
    input_file = CWD.joinpath(filename)
    return np.pad(np.genfromtxt(input_file, delimiter=1, dtype=np.uint8), ((1,1),(1,1)), mode='constant', constant_values=9)


def low_points(inp: np.ndarray) -> List[Tuple[int, int]]:
    mask = generic_filter(inp, lambda x: x[2] < min(x[:2]) and x[2] < min(x[3:]), footprint=[[0,1,0],[1,1,1],[0,1,0]], mode="constant", cval=9)
    return [(x,y) for (x, y), item in np.ndenumerate(mask) if item != 0]


@show
def first(inp: np.ndarray, lows: List[Tuple[int, int]]) -> int:
    return sum(inp[coord] + 1 for coord in lows)


def basin(inp: np.ndarray, x: int, y: int) -> int:
    inp[x, y] = 100
    def rec(x2, y2) -> int:
        neighbor = inp[x2, y2]
        if neighbor < 9:
            return basin(inp, x2, y2)
        return 0
    return 1 + rec(x - 1, y) + rec(x + 1, y) + rec(x, y - 1) + rec(x, y + 1)


@show
def second(inp: np.ndarray, lows: List[Tuple[int, int]]) -> int:
    sizes = [basin(inp, x, y) for x, y in lows]
    return reduce(lambda x, y: x * y, sorted(sizes)[-3:])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        lows = low_points(inp)
        assert first(inp, lows) == 15
        assert second(inp, lows) == 1134


if __name__ == "__main__":
    test_example()
    inp = read_input()
    lows = low_points(inp)
    first(inp, lows)  # 506
    second(inp, lows)  # 931200

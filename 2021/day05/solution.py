#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import *

import numpy as np
from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [int(s) for l in reader.readlines() for s in l.strip().replace(" -> ", ",").split(",")]


def get_range(a: int, b: int, nb: int) -> List[int]:
    if a == b:
        return [a] * nb
    if a < b:
        return [i for i in range(a, b + 1)]
    return [i for i in range(a, b - 1, -1)]


def build_grid(inp: List[int], diag: bool = False) -> np.ndarray:
    size = max(inp) + 1
    arr = np.zeros((size, size), dtype=int)
    for i in range(len(inp) // 4):
        idx = i * 4
        x1, y1, x2, y2 = inp[idx], inp[idx + 1], inp[idx + 2], inp[idx + 3]
        if not diag and not ((x1 == x2) or (y1 == y2)):
            continue
        xrange = get_range(x1, x2, abs(y1 - y2) + 1)
        yrange = get_range(y1, y2, abs(x1 - x2) + 1)
        for x, y in zip(xrange, yrange):
            arr[y, x] += 1
    return arr


@show
def first(inp: List[int]) -> int:
    return len([n for n in build_grid(inp).flatten() if n >= 2])


@show
def second(inp: List[int]) -> int:
    return len([n for n in build_grid(inp, True).flatten() if n >= 2])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 5
        assert second(inp) == 12


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 6267
    second(inp)  # 20196

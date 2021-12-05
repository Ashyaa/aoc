#!/usr/bin/env python3

import contextlib
import numpy as np

from pathlib import Path

from typing import *

from numpy.core.defchararray import count
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            t1, t2 = l.strip().split(" -> ")
            res.extend(
                [
                    int(t1.split(",")[0]),
                    int(t1.split(",")[1]),
                    int(t2.split(",")[0]),
                    int(t2.split(",")[1]),
                ]
            )
        return res


def build_grid(inp: List[int], diag: bool = False) -> np.ndarray:
    size = max(inp) + 1
    arr = np.zeros((size, size), dtype=int)
    for i in range(len(inp) // 4):
        idx = i * 4
        if inp[idx] == inp[idx + 2]:
            mn, mx = (
                min(inp[idx + 1], inp[idx + 3]),
                max(inp[idx + 1], inp[idx + 3]) + 1,
            )
            arr[mn:mx, inp[idx]] += 1
        elif inp[idx + 1] == inp[idx + 3]:
            mn, mx = min(inp[idx], inp[idx + 2]), max(inp[idx], inp[idx + 2]) + 1
            arr[inp[idx + 1], mn:mx] += 1
        elif diag:
            if inp[idx] < inp[idx + 2]:
                xrange = [i for i in range(inp[idx], inp[idx + 2] + 1)]
            else:
                xrange = [i for i in range(inp[idx], inp[idx + 2] - 1, -1)]
            if inp[idx + 1] < inp[idx + 3]:
                yrange = [i for i in range(inp[idx + 1], inp[idx + 3] + 1)]
            else:
                yrange = [i for i in range(inp[idx + 1], inp[idx + 3] - 1, -1)]
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

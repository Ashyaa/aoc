#!/usr/bin/env python3

from collections import defaultdict
import contextlib

import numpy as np
from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Dict[int, int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        unique, counts = np.unique([int(n) for n in reader.readline().split(',')], return_counts=True)
        return dict(zip(unique, counts))


def loop(inp: DefaultDict[int, int], days: int) -> DefaultDict[int, int]:
    for _ in range(days):
        new_day = defaultdict(int)
        for i in range(9):
            if i == 0:
                new_day[6] += inp[i]
                new_day[8] += inp[i]
            else:
                new_day[i-1] += inp[i]
        inp = new_day
    return inp


@show
def first(inp: Dict[int, int], days: int) -> int:
    return sum(loop(defaultdict(int, inp), days).values())


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp, 18) == 26
        assert first(inp, 80) == 5934
        assert first(inp, 256) == 26984457539


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp, 80)  # 386536
    first(inp, 256)  # 1732821262171

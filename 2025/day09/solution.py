#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List, Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [tuple(map(int, line.strip().split(","))) for line in reader.readlines()]


@show
def first(inp: List[Tuple[int, int]]) -> int:
    res = []
    for i, (x1, y1) in enumerate(inp):
        for j in range(i + 1, len(inp)):
            x2, y2 = inp[j]
            res.append(abs(x1 - x2 + 1) * abs(y1 - y2 + 1))
    return max(res)


@show
def second(inp: List[Tuple[int, int]]) -> int:
    # map all possiblites with their area, then sort by descending area
    # find the first couple that has no point outside the polygon
    return 0


def test_example() -> None:
    inp = read_input("example.txt")
    print(inp)
    with contextlib.redirect_stdout(None):
        assert first(inp) == 50
        assert second(inp) == 24


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # p1
    second(inp)  # p2

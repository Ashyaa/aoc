#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List, Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[str, int]]:
    input_file = CWD.joinpath(filename)
    res = []
    with open(input_file, "r") as reader:
        for line in reader.readlines():
            res.append((line[0], int(line[1:])))
    return res


@show
def first(inp) -> int:
    pos = 50
    res = 0
    for dir, nb in inp:
        pos = (pos + nb if dir == "R" else pos - nb) % 100
        if (pos % 100) == 0:
            res += 1
    return res


@show
def second(inp) -> int:
    pos = 50
    res = 0
    for dir, nb in inp:
        if dir == "R":
            res += (nb + pos) // 100
        else:
            res += abs(-nb - pos) // 100
        pos = (pos + nb if dir == "R" else pos - nb) % 100
    return res


def test_example() -> None:
    assert (abs(50 - 1000) // 100) + (50 < 1000) == 10
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 3
    assert second(inp) == 6


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # p1
    second(inp)  # p2

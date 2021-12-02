#!/usr/bin/env python3

import contextlib

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[Tuple[int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            val = int(l.split(" ")[-1])
            if l.startswith("up"):
              res.append((0, -val))
            elif l.startswith("down"):
              res.append((0, val))
            else:
              res.append((val, 0))
        return res


@show
def first(input: List[Tuple[int, int]]) -> int:
    x, z = 0, 0
    for dx, dz in input:
        x += dx
        z += dz
    return x * z


@show
def second(input: List[Tuple[int, int]]) -> int:
    x, z, aim = 0, 0, 0
    for dx, dz in input:
        x += dx
        aim += dz
        z += dx * aim
    return x * z


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        ex = read_input("example.txt")
        assert first(ex) == 150
        assert second(ex) == 900


if __name__ == "__main__":
    input = read_input()
    test_example()
    first(input)  # 1804520
    second(input)  # 1971095320

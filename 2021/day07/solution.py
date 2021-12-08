#!/usr/bin/env python3

import contextlib

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [int(n) for n in reader.readline().split(',')]


def cost(inp: List[int], pos: int) -> int:
    return sum([abs(i - pos) for i in inp])

def cost_2(inp: List[int], pos: int) -> int:
    sigma = lambda n: n * (n+1) // 2
    return sum([sigma(abs(i - pos)) for i in inp])

@show
def first(inp: List[int]) -> int:
    return min([cost(inp, i) for i in range(min(inp), max(inp)+1)])


@show
def second(inp: List[int]) -> int:
    return min([cost_2(inp, i) for i in range(min(inp), max(inp)+1)])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 37
        assert second(inp) == 168


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 348996
    second(inp)  # 98231647

#!/usr/bin/env python3

from pathlib import Path
from typing import Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> None:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        pass


def solve(inp) -> Tuple[int, int]:
    return 0, 0


def test_example() -> None:
    inp = read_input("example.txt")
    assert (r := solve(inp)) == (0, 0), r


if __name__ == "__main__":
    test_example()
    show(solve)(read_input())  # p1, p2

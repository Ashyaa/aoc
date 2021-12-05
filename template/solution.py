#!/usr/bin/env python3

import contextlib

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> None:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        pass


@show
def first(inp) -> None:
    pass


@show
def second(inp) -> None:
    pass


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == None
        assert second(inp) == None


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # p1
    second(inp)  # p2

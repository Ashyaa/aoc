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
def first(input) -> None:
    pass


@show
def second(input) -> None:
    pass


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first() == None
        assert second() == None


if __name__ == "__main__":
    input = read_input()
    test_example()
    first(input)  # p1
    second(input)  # p2

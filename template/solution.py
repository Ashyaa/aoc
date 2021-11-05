#!/usr/bin/env python3

import contextlib

from pathlib import Path

# from typing import ...
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> None:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        pass


@show
def first() -> None:
    pass


@show
def second() -> None:
    pass


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first() == None
        assert second() == None


if __name__ == "__main:":
    test_example()
    first()  # p1
    second()  # p2

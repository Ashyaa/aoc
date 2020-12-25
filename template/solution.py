#!/usr/bin/env python3

from pathlib import Path
# from typing import ...
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> None:
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
    assert first() == None
    assert second() == None


test_example()
first() # p1
second() # p2
#!/usr/bin/env python3
"""
Day solved visually. The harsh limitations in choice movements make it so that very few solutions actually exist.
By finding one, and improving the cost efficiency, I was able to find both solutions without code.
"""

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> None:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        pass


@show
def first() -> int:
    """
    5 + 5 + 50 + 40 + 200 + 500 + 6000 + 500 + 200 + 9000 + 3 + 3
    = 16506
    """
    return 16506


@show
def second() -> int:
    """
    7 + 500 + 40 + 8 + 50 +60 + 50 + 50 + 8 + 5000 + 500 + 600 +
    3 + 700 + 700 + 7000 + 11000 + 11000 + 11000 + 5 + 5 + 9 + 9
    = 48704
    """
    return 48304


if __name__ == "__main__":
    first()  # 16506
    second()  # 48304

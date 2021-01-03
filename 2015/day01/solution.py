#!/usr/bin/env python3

import contextlib

from pathlib import Path
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> None:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return reader.read().strip()


@show
def first(s: str) -> int:
    return s.count("(") - s.count(")")


@show
def second(s: str) -> int:
    i, flr = 1, 0
    for c in s:
        flr = flr + 1 if c == '(' else flr - 1
        if flr == -1:
            return i
        i += 1


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first("(())") == first("()()") ==  0
        assert first("(((") == first("(()(()(") == first("))(((((") == 3
        assert first("())") == first("))(") == -1
        assert first(")))") == first(")())())") == -3
        assert second(")") == 1
        assert second("()())") == 5


test_example()
s = read_input()
first(s) # 280
second(s) # 1797
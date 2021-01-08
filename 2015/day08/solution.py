#!/usr/bin/env python3

import contextlib
import re

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent

HEX_REGEX = re.compile(r"\\x[\da-f]{2}")

def read_input(filename: str="input.txt") -> str:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return reader.read().split("\n")


def count(s: str) -> int:
    actual = s[1:-1].replace("\\\"", "_").replace("\\\\", "_")
    actual = HEX_REGEX.sub("?", actual)
    return len(s) - len(actual)


@show
def first(arr: List[str]) -> int:
    return sum([count(s.strip()) for s in arr])


def count_2(s: str) -> int:
    actual = s.replace("\\", "\\\\").replace("\"", "\\\"")
    return 2 + len(actual) - len(s)


@show
def second(arr: List[str]) -> int:
    return sum([count_2(s.strip()) for s in arr])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        s = read_input("example.txt")
        assert count(s[0]) == 2
        assert count(s[1]) == 2
        assert count(s[2]) == 3
        assert count(s[3]) == 5
        assert first(s) == 12
        assert count_2(s[0]) == 4
        assert count_2(s[1]) == 4
        assert count_2(s[2]) == 6
        assert count_2(s[3]) == 5
        assert second(s) == 19


test_example()
s = read_input()
first(s) # 1342
second(s) # 2074
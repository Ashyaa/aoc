#!/usr/bin/env python3

import contextlib

from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[List[str]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [l.strip().replace(" | ", " ").split(" ") for l in reader.readlines()]


def decode(line: List[str]) -> int:
    cur_digits = [None] * 10
    for i, wanted in zip([1,4,7,8], [2,4,3,7]):
        cur_digits[i] = next(set(w) for w in line if len(w) == wanted)
    cur_digits[3] = next(set(w) for w in line if len(w) == 5 and cur_digits[7] < set(w))
    cur_digits[5] = next(set(w) for w in line if len(w) == 5 and set(w) != cur_digits[3] and set(w) < cur_digits[9])
    cur_digits[2] = next(set(w) for w in line if len(w) == 5 and set(w) != cur_digits[3] and set(w) != cur_digits[5])
    cur_digits[9] = next(set(w) for w in line if len(w) == 6 and cur_digits[3] < set(w))
    cur_digits[6] = next(set(w) for w in line if len(w) == 6 and set(w) != cur_digits[9] and cur_digits[5] < set(w))
    cur_digits[0] = next(set(w) for w in line if len(w) == 6 and set(w) != cur_digits[6] and set(w) != cur_digits[9])
    return int("".join(str(cur_digits.index(set(w))) for w in line[-4:]))


@show
def first(inp: List[str]) -> int:
    return len([w for l in inp for w in l[-4:] if len(w) in [2,4,3,7]])


@show
def second(inp: List[str]) -> int:
    return sum(decode(l) for l in inp)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 26
        assert decode("acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab cdfeb fcadb cdfeb cdbaf".split(" ")) == 5353
        assert second(inp) == 61229


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)
    second(inp)

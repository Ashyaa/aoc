#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[List[int]]:
    input_file = CWD.joinpath(filename)
    res = []
    with open(input_file, "r") as reader:
        res = [[int(c) for c in line.strip()] for line in reader.readlines()]
    return res


def max_joltage(bank: List[int], depth: int):
    joltage = ""
    cur_idx = 0
    while len(joltage) < depth:
        max_idx = len(bank) - depth + len(joltage) + 1
        max_digit = max(bank[cur_idx:max_idx])
        idx = bank[cur_idx:max_idx].index(max_digit)

        joltage += str(max_digit)
        cur_idx += idx + 1
    return int(joltage)


@show
def first(inp: List[List[int]]) -> int:
    return sum(max_joltage(b, 2) for b in inp)


@show
def second(inp: List[List[int]]) -> int:
    return sum(max_joltage(b, 12) for b in inp)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 357
        assert second(inp) == 3121910778619


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 17430
    second(inp)  # 171975854269367

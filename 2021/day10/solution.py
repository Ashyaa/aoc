#!/usr/bin/env python3

import contextlib

from functools import reduce
from pathlib import Path

from typing import *
from AoC.util import show


CWD = Path(__file__).parent
SCORES = {')': 3, ']': 57, '}': 1197, '>': 25137}
SCORES_2 = {')': 1, ']': 2, '}': 3, '>': 4}
MATCHING = {'(': ')', '[': ']', '{': '}', '<': '>'}


def read_input(filename: str = "input.txt") -> List[str]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [l.strip() for l in reader.readlines()]


def find_matching(l: str, idx: int) -> int:
    lvl = 0
    for i, c in enumerate(l[idx+1:]):
        if c in MATCHING:
            lvl += 1
        else:
            if lvl == 0:
                return i+idx+1
            lvl -= 1
    return -1


@show
def first(inp: List[str]) -> int:
    res = 0
    for l in inp:
        closers = []
        for j, c in enumerate(l):
            if c not in MATCHING:
                continue
            idx = find_matching(l, j)
            if idx < 0 or MATCHING[c] == l[idx]:
                continue
            closers.append(idx)
        if closers:
            res += SCORES[l[min(closers)]]
    return res


@show
def second(inp: List[str]) -> int:
    res = []
    for l in inp:
        closers = []
        for j, c in enumerate(l):
            if c not in MATCHING:
                continue
            idx = find_matching(l, j)
            if idx >= 0:
                if MATCHING[c] != l[idx]: # corrupted
                    closers = []
                    break
                continue
            closers.append(SCORES_2[MATCHING[c]])
        if closers:
            res.append(reduce(lambda x, y: x * 5 + y, [0]+closers[::-1]))
    return sorted(res)[len(res)//2]


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 26397
        assert second(inp) == 288957


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 318099
    second(inp)  # 2389738699

#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> List[Tuple[int, int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        res = []
        for l in reader.readlines():
            dims = [int(x) for x in l.split("x")]
            res.append(tuple(dims))
        return res


@show
def first(boxes: List[Tuple[int, int, int]]) -> None:
    res = 0
    for l, w, h in boxes:
        sides = [l*w, l*h, w*h]
        res += 2*sum(sides) + min(sides)
    return res


@show
def second(boxes: List[Tuple[int, int, int]]) -> None:
    res = 0
    for l, w, h in boxes:
        sides = [l+w, l+h, w+h]
        res += 2*min(sides) + l*w*h
    return res


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first([(2, 3, 4)]) == 58
        assert first([(1, 1, 10)]) == 43
        assert second([(2, 3, 4)]) == 34
        assert second([(1, 1, 10)]) == 14


test_example()
boxes = read_input()
first(boxes) # 1588178
second(boxes) # p2
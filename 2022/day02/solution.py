#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List
from AoC.util import show


CWD = Path(__file__).parent

ITEMS = ["A","B","C"]

PLAYS = ["X","Y","Z"]


get_index = lambda l, item: next(i for i, it in enumerate(l) if it == item)


def read_input(filename: str = "input.txt") -> List[List[str]]:
    with open(CWD.joinpath(filename), "r", encoding="utf-8") as reader:
        return [l.strip().split(" ") for l in reader.readlines()]


def score_1(p1: str, p2: str) -> int:
    index_p1 = get_index(ITEMS, p1)
    index_p2 = get_index(PLAYS, p2)
    if index_p2 == index_p1:
        return 3 + index_p2+1
    if (index_p2-1) % 3 == index_p1:
        return 6 + index_p2+1
    return index_p2+1


def score_2(p1: str, p2: str) -> int:
    index_p1 = get_index(ITEMS, p1)
    index_p2 = get_index(PLAYS, p2)
    to_play = (index_p1 + index_p2 - 1) % 3
    return 1 + get_index(ITEMS, ITEMS[to_play]) + index_p2 * 3


@show
def first(l: List[List[str]]) -> int:
    return sum(score_1(*game) for game in l)


@show
def second(l: List[List[str]]) -> int:
    return sum(score_2(*game) for game in l)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        r1  = first(inp)
        assert r1 == 15, r1
        r2  = second(inp)
        assert r2 == 12, r2


test_example()
s = read_input()
first(s)  # 13009
second(s)  # 10398

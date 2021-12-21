#!/usr/bin/env python3

import contextlib
from itertools import product
from pathlib import Path

import numpy as np

from typing import *
from AoC.util import show


CWD = Path(__file__).parent

CACHE = {}

def read_input(filename: str = "input.txt") -> Tuple[int, int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        p1 = int(reader.readline().strip()[28:])
        p2 = int(reader.readline().strip()[28:])
        return p1, p2


def deterministic(dice: int, pos: int, score: int) -> Tuple[int, int, int]:
    move = 0
    for _ in range(3):
        dice = ((dice) % 100) + 1
        move += dice
    move = ((pos + move -1) % 10) +1
    return dice, move, score + move


@show
def first(p1: int, p2: int) -> int:
    dice, turn = 0, True
    rolls = 0
    s1, s2 = 0, 0
    while s1 < 1000 and s2 < 1000:
        if turn:
            dice, p1, s1 = deterministic(dice, p1, s1)
        else:
            dice, p2, s2 = deterministic(dice, p2, s2)
        turn = not turn
        rolls += 3
    return min(s1, s2) * rolls


uni, cts = np.unique([r1+r2+r3 for r1, r2, r3 in product(range(1,4),range(1,4),range(1,4))], return_counts=True)
DIRAC_ROLLS = list(zip(uni, cts))


def dirac(p1: int, s1: int, p2: int, s2: int, turn: bool) -> Tuple[int, int]:
    if s1 >= 21:
        return 1,0
    if s2 >= 21:
        return 0,1
    win1, win2 = 0, 0
    if (p1, s1, p2, s2, turn) in CACHE:
        return CACHE[(p1, s1, p2, s2, turn)]
    for roll, times in DIRAC_ROLLS:
        sub_p1, sub_p2 = p1, p2
        sub_s1, sub_s2 = s1, s2
        if turn:
            sub_p1 = ((p1+roll-1) % 10) + 1
            sub_s1 += sub_p1
        else:
            sub_p2 = ((p2+roll-1) % 10) + 1
            sub_s2 += sub_p2
        w1, w2 = dirac(sub_p1, sub_s1, sub_p2, sub_s2, not turn)
        win1 +=  w1 * times
        win2 +=  w2 * times
    CACHE[(p1, s1, p2, s2, turn)] = (win1, win2)
    return win1, win2


@show
def second(p1: int, p2: int) -> int:
    r1, r2 = dirac(p1, 0, p2, 0, True)
    return max(r1, r2)


def test_example() -> None:
    inp = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert first(*inp) == 739785
        assert second(*inp) == 444356092776315


if __name__ == "__main__":
    test_example()
    CACHE = {}
    inp = read_input()
    first(*inp)  # 605070
    second(*inp)  # 218433063958910

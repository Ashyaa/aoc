#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import *

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[List[str]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [[c for c in l.strip()] for l in reader.readlines()]


def move(inp: List[List[str]], elts: List[Tuple[int,int]], east: bool) -> Tuple[List[List[str]], bool]:
    res, changes = False, {}
    size_x, size_y = len(inp), len(inp[0])
    for x, y in elts:
        val = inp[x][y]
        x1, y1 = x, y
        if east:
            y1 = (y+1) % size_y
        else:
            x1 = (x+1) % size_x
        if inp[x1][y1] == '.':
            changes[(x1, y1)] = val
            changes[(x, y)] = '.'
            res = True
        else:
            changes[(x, y)] = val
    for (x,y), val in changes.items():
        inp[x][y] = val
    return inp, res


def list_elts(inp: List[List[str]]) -> Tuple[List[Tuple[int,int]], List[Tuple[int,int]]]:
    east, south = [], []
    for x in range(len(inp)):
        for y in range(len(inp[0])):
            if inp[x][y] == '>':
                east.append((x,y))
            if inp[x][y] == 'v':
                south.append((x,y))
    return east, south


@show
def first(inp: List[List[str]]) -> int:
    step, moved = 0, True
    while moved:
        step += 1
        east, south = list_elts(inp)
        moved = False
        inp, has_moved = move(inp, east, True)
        moved = moved or has_moved
        inp, has_moved = move(inp, south, False)
        moved = moved or has_moved
    return step


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert first(inp) == 58


if __name__ == "__main__":
    test_example()
    inp = read_input()
    first(inp)  # 384

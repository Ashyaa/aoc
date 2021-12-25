#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import *
import numpy as np
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> np.ndarray:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        lines = reader.readlines()
        x, y = len(lines), 0
        res = []
        for l in lines:
            if y == 0:
                y = len(l.strip())
            res.extend(c for c in l.strip())
        r = np.array(res).reshape((x,y))
        return r


def move(inp: np.ndarray, elts: List[Tuple[int,int]], east: bool) -> Tuple[np.ndarray, bool]:
    res = False
    changes = {}
    for x, y in elts:
        val = inp[x,y]
        next_pos = x, y
        if east:
            next_pos = x, (y+1) % inp.shape[1]
        else:
            next_pos = (x+1) % inp.shape[0], y
        if inp[next_pos] == '.':
            changes[next_pos] = val
            changes[(x, y)] = '.'
            res = True
        else:
            changes[x, y] = val
    for pos, val in changes.items():
        inp[pos] = val
    return inp, res


def list_elts(inp: np.ndarray) -> Tuple[List[Tuple[int,int]], List[Tuple[int,int]]]:
    east, south = [], []
    for x in range(inp.shape[0]):
        for y in range(inp.shape[1]):
            if inp[x,y] == '>':
                east.append((x,y))
            if inp[x,y] == 'v':
                south.append((x,y))
    return east, south


@show
def first(inp: np.ndarray) -> int:
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

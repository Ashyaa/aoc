#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> str:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return reader.read()


move = {
    "^": lambda x, y: (x+1, y),
    ">": lambda x, y: (x, y+1),
    "v": lambda x, y: (x-1, y),
    "<": lambda x, y: (x, y-1),
}

@show
def first(s: str) -> None:
    coord = 0, 0
    visited = set()
    visited.add(coord)
    for c in s:
        coord = move[c](*coord)
        visited.add(coord)
    return len(visited)


@show
def second(s: str) -> None:
    coord = 0, 0
    r_coord = coord
    visited = set()
    visited.add(coord)
    for i, c in enumerate(s):
        if i % 2 == 0:
            cur = coord = move[c](*coord)
        else:
            cur = r_coord = move[c](*r_coord)
        visited.add(cur)
    return len(visited)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        assert first(">") == first("^v^v^v^v^v") == 2
        assert first("^>v<") == 4
        assert second("^v") == second("^>v<") == 3
        assert second("^v^v^v^v^v") == 11


test_example()
s = read_input()
first(s) # 2592
second(s) # 2360
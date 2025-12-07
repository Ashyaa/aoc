#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List, Set, Tuple

from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> List[str]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [line.strip() for line in reader.readlines()]


def splits_p1(x, y, splitters, max_x) -> Set:
    if x == max_x:
        return set()
    if (x, y) not in splitters:
        return splits_p1(x + 1, y, splitters, max_x)
    if splitters[(x, y)] is None:
        splitters[(x, y)] = (
            set([(x, y)]) | splits_p1(x, y - 1, splitters, max_x) | splits_p1(x, y + 1, splitters, max_x)
        )
    return splitters[(x, y)]


def splits_p2(x, y, splitters, max_x) -> int:
    if x == max_x:
        return 1
    if (x, y) not in splitters:
        return splits_p2(x + 1, y, splitters, max_x)
    if splitters[(x, y)] is None:
        splitters[(x, y)] = splits_p2(x, y - 1, splitters, max_x) + splits_p2(x, y + 1, splitters, max_x)
    return splitters[(x, y)]


@show
def solve(inp: List[str]) -> Tuple[int, int]:
    start = inp[0].index("S")
    splitters = {}
    for x, s in enumerate(inp):
        for y, c in enumerate(s):
            if c == "^":
                splitters[(x, y)] = None
    return len(splits_p1(0, start, splitters.copy(), len(inp) - 1)), splits_p2(0, start, splitters, len(inp) - 1)


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        assert solve(inp) == (21, 40)


if __name__ == "__main__":
    # test_example()
    inp = read_input()
    solve(inp)  # 1553, 15811946526915

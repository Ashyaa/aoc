#!/usr/bin/env python3

import contextlib
from itertools import product
from pathlib import Path
from typing import Any, Generator, List, Tuple

from AoC.util import show

CWD = Path(__file__).parent

OFFSETS = [(dx, dy) for dx, dy in product(range(-1, 2), range(-1, 2))]


def read_input(filename: str = "input.txt") -> List[str]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [line.strip() for line in reader.readlines()]


def neighbours(
    x: int, y: int, height: int, width: int
) -> Generator[Tuple[int, int], Any, None]:
    for dx, dy in OFFSETS:
        if dx == dy == 0:
            continue
        nx, ny = x + dx, y + dy
        if 0 <= nx < height and 0 <= ny < width:
            yield (nx, ny)


def iteration(inp: List[str], height: int, width: int) -> Tuple[List[str], int]:
    removed = 0
    res = [s for s in inp]
    for x, y in product(range(0, width), range(0, height)):
        if inp[x][y] != "@":
            continue
        adjacents = sum(
            inp[nx][ny] == "@" for nx, ny in neighbours(x, y, height, width)
        )
        if adjacents < 4:
            res[x] = res[x][:y] + "." + res[x][y + 1 :]
            removed += 1
    return res, removed


@show
def solve(inp: List[str]) -> Tuple[int, int]:
    first, second = 0, 0
    height, width = len(inp), len(inp[0])
    while True:
        inp, removed = iteration(inp, height, width)
        if removed == 0:
            break
        if not first:
            first = removed
        second += removed

    return first, second


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        inp = read_input("example.txt")
        p1, p2 = solve(inp)
        assert p1 == 13
        assert p2 == 43


if __name__ == "__main__":
    test_example()
    inp = read_input()
    solve(inp)  # 1478, 9120

#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List, Tuple

import numpy as np
from AoC.util import show

CWD = Path(__file__).parent


def read_input(filename: str = "input.txt") -> Tuple[List[int], List[np.ndarray]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        numbers = [int(w) for w in reader.readline().split(",")]
        grids = [
            np.array(
                [int(n) for l in gr.split("\n") for n in " ".join(l.split()).split(" ")]
            ).reshape(5, 5)
            for gr in "".join(reader.readlines()[1:]).split("\n\n")
        ]
        return numbers, grids


@show
def first(numbers: List[int], grids: List[np.ndarray]) -> int:
    for i in range(5, len(numbers)):
        cur_numbers = set(numbers[:i])
        for grid in grids:
            for j in range(5):
                if set(grid[:, j]).issubset(cur_numbers) or set(grid[j, :]).issubset(
                    cur_numbers
                ):
                    return sum(set(grid.flatten()) - cur_numbers) * numbers[i - 1]
    return 0


@show
def second(numbers: List[int], grids: List[np.ndarray]) -> int:
    def winning_when(numbers: List[int], grid: np.ndarray) -> int:
        for i in range(5, len(numbers)):
            cur_numbers = set(numbers[:i])
            for j in range(5):
                if set(grid[:, j]).issubset(cur_numbers) or set(grid[j, :]).issubset(
                    cur_numbers
                ):
                    return i
        return -1

    order = [winning_when(numbers, grid) for grid in grids]
    last_i = max(order)
    last_grid = grids[order.index(last_i)]
    return sum(set(last_grid.flatten()) - set(numbers[:last_i])) * numbers[last_i - 1]


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        i1, i2 = read_input("example.txt")
        assert first(i1, i2) == 4512
        assert second(i1, i2) == 1924


if __name__ == "__main__":
    test_example()
    i1, i2 = read_input()
    first(i1, i2)  # 33348
    second(i1, i2)  # 8112

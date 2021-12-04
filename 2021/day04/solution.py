#!/usr/bin/env python3

import contextlib
from pathlib import Path
from typing import List

import numpy as np
from AoC.util import show

CWD = Path(__file__).parent


def play(numbers: List[int], grids: List[np.ndarray]) -> List[int]:
    res = []
    for grid in grids:
        won = False
        for i in range(5, len(numbers)):
            cur_numbers = set(numbers[:i])
            for j in range(5):
                if set(grid[:, j]).issubset(cur_numbers) or set(grid[j, :]).issubset(
                    cur_numbers
                ):
                    res.append(
                        (i, sum(set(grid.flatten()) - cur_numbers) * numbers[i - 1])
                    )
                    won = True
                    break
            if won:
                break
    return [score for _, score in sorted(res, key=lambda tup: tup[0])]


def read_input(filename: str = "input.txt") -> List[int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        numbers = [int(w) for w in reader.readline().split(",")]
        grids = [
            np.array(
                [int(n) for l in gr.split("\n") for n in " ".join(l.split()).split(" ")]
            ).reshape(5, 5)
            for gr in "".join(reader.readlines()[1:]).split("\n\n")
        ]
        return play(numbers, grids)


@show
def first(scores: List[int]) -> int:
    return scores[0]


@show
def second(scores: List[int]) -> int:
    return scores[-1]


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        scores = read_input("example.txt")
        assert first(scores) == 4512
        assert second(scores) == 1924


if __name__ == "__main__":
    test_example()
    scores = read_input()
    first(scores)  # 33348
    second(scores)  # 8112

#!/usr/bin/env python3

import contextlib

from pathlib import Path
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> List[Tuple[int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        r = [int(l) for l in reader.readlines()]
        r.sort()
        return [(c, i) for i, c in enumerate(r)]


def candidates(cs: List[Tuple[int, int]], total: int=150, recursed=False):
    for i, c in enumerate(cs):
        left = total - c[0]
        if left < 0:
            break
        if left == 0:
            yield [c[1]]
            continue
        partial = cs[:i] + cs [i+1:]
        if not recursed:
            partial = cs [i+1:]
        for y in candidates(partial, left, True):
            yield [c[1]] + y


@show
def solve(containers: List[int], target: int=150) -> int:
    combinations = candidates(containers, target)
    res = set()
    for combi in combinations:
        combi.sort()
        res.add(tuple(combi))
    min_nb = min([len(s) for s in res])
    return len(res), len([s for s in res if len(s) == min_nb])


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        example = read_input("example.txt")
        assert solve(example, 25) == (4, 3)


test_example()
containers = read_input()
solve(containers) # 1638, 17
#!/usr/bin/env python3

import contextlib
from collections import defaultdict

from pathlib import Path
from numpy import vectorize
from typing import List, Tuple
from AoC.util import show


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> List[Tuple[int, int]]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        r = [int(l) for l in reader.readlines()]
        r.sort()
        return [(c, i) for i, c in enumerate(r)]


def candidates(cs: List[Tuple[int, int]], total: int=150, recursed: bool=False):
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
def solve(containers: List[Tuple[int, int]], target: int=150) -> Tuple[int, int]:
    """Optimized solution based on candidate generator"""
    combinations = candidates(containers, target)
    res = set()
    for combi in combinations:
        combi.sort()
        res.add(tuple(combi))
    min_nb = min([len(s) for s in res])
    return len(res), len([s for s in res if len(s) == min_nb])


@show
def quick_solve() -> Tuple[int, int]:
    """Optimized solution using bitmasks to represent the input"""
    dimensions = vectorize(int)(list(open('input.txt')))
    res = defaultdict(int)
    for mask in range(1, 1<<len(dimensions)):
        p = [d for i,d in enumerate(dimensions) if (mask & (1 << i)) > 0]
        if sum(p) == 150: res[len(p)] += 1
    return sum(res.values()), res[min(res.keys())]


def test_example() -> None:
    with contextlib.redirect_stdout(None):
        example = read_input("example.txt")
        assert solve(example, 25) == (4, 3)


test_example()
containers = read_input()
quick_solve() # 1638, 17
solve(containers) # 1638, 17
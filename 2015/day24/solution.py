#!/usr/bin/env python3
""" Solution implemented using explanations and bits of code from https://www.geeksforgeeks.org/subset-sum-problem-dp-25/"""
import contextlib
import numpy as np
from functools import reduce

from pathlib import Path
from typing import Iterator, List
from AoC.util import show
from numpy.core.defchararray import find


CWD = Path(__file__).parent


def read_input(filename: str="input.txt") -> List[int]:
    input_file = CWD.joinpath(filename)
    with open(input_file, "r") as reader:
        return [int(x) for x in reader]


def dp(packages: List[int], target: int) -> np.ndarray:
    n = len(packages)
    subset = np.zeros((n+1, target+1), dtype=bool)
    subset[::,0] = True

    for i in range(1, n + 1):
        for j in range(1, target + 1):
            if j < packages[i-1]:
                subset[i,j] = subset[i-1,j]
            if j>= packages[i-1]:
                subset[i,j] = subset[i-1,j] or subset[i-1,j-packages[i-1]]
    return subset


def candidates(packages: List[int], index: int, target: int, dp: np.ndarray, cur: List[int]) -> Iterator[List[int]]:
    if index <= 0 and target != 0 and dp[0, target]:
        yield cur
        return
    if index <= 0 and target == 0:
        yield cur
        return
    if dp[index,target]:
        for r in candidates(packages, index-1, target, dp, cur):
            yield r
    if target >= packages[index] and dp[index,target-packages[index]]:
        new_cur = cur + [packages[index]]
        for r in candidates(packages, index-1, target-packages[index], dp, new_cur):
            yield r


def get_candidates(packages: List[int], target: int) -> Iterator[List[int]]:
    matrix = dp(packages, target)
    return candidates(packages, len(packages)-1, target, matrix, [])


qe = lambda arr: reduce(lambda x, y: x*y, arr)


@show
def first(packages: List[int]) -> int:
    groups = [(len(g), qe(g)) for g in get_candidates(packages, sum(packages)//3)]
    min_len = min(groups, key=lambda t: t[0])[0]
    smallest_groups = [q_e for l, q_e in groups if l == min_len]
    return min(smallest_groups)


@show
def second(packages: List[int]) -> int:
    groups = [(len(g), qe(g)) for g in get_candidates(packages, sum(packages)//4)]
    min_len = min(groups, key=lambda t: t[0])[0]
    smallest_groups = [q_e for l, q_e in groups if l == min_len]
    return min(smallest_groups)


def test_example() -> None:
    packages = read_input("example.txt")
    with contextlib.redirect_stdout(None):
        assert first(packages) == 99
        assert second(packages) == 44


test_example()
packages = read_input()
first(packages) # 10439961859
second(packages) # 72050269